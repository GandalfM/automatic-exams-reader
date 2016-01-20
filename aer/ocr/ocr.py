from PIL import Image
from sklearn.externals import joblib
from skimage.feature import hog
import numpy as np
from aer.utils.imageutil import *
import cv2
import pytesseract


class Ocr:
    __CLASSIFIER_FILE_NAME = "cls.pkl"
    __TESSERACT_CONFIG_FILENAME = "tesseract-config"
    __TO_WHITE_BLACK_THRESHOLD = 100

    def __init__(self):
        self.clf = None
        parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.__CLASSIFIER_FILE = os.path.join(parent_dir, self.__CLASSIFIER_FILE_NAME)
        self.__TESSERACT_CONFIG = os.path.join(parent_dir, self.__TESSERACT_CONFIG_FILENAME)
        self.connectivity = 4

    def load_classifier(self):
        if not os.path.isfile(self.__CLASSIFIER_FILE):
            raise Exception("Please, create a classifier first. Create will be created after running file learn_classifier.py")
        else:
            self.clf = joblib.load(self.__CLASSIFIER_FILE)

    def filter_biggest_blob(self, image):
        _, labels, stats, _ = cv2.connectedComponentsWithStats(image, self.connectivity)
        if len(stats) == 1:
            return image
        tmp = np.argwhere(stats[1:, 4] == max(stats[1:, 4]))
        idx = (labels == tmp[0][0] + 1)
        mask = np.zeros(image.shape, np.uint8)
        mask.fill(0)
        mask[idx] = 255
        return mask

    def isImageEmpty(self, image, maxBlobSize):
        imageSize = image.shape[0] * image.shape[1]
        return 0.01 * imageSize > maxBlobSize

    def filter_big_blobs(self, image):
        _, labels, stats, _ = cv2.connectedComponentsWithStats(image, self.connectivity)
        if len(stats) == 1:
            return image
        maxSize = max(stats[1:, 4])
        if self.isImageEmpty(image, maxSize):
            return None

        tmp = np.argwhere(stats[1:, 4] > 0.5 * maxSize)
        idx = (labels == tmp[0][0] + 1)
        mask = np.zeros(image.shape, np.uint8)
        mask.fill(0)
        mask[idx] = 255
        return mask

    def trim_image(self, image):
        non_zero_y, non_zero_x = np.nonzero(image)
        min_x = np.amin(non_zero_x)
        max_x = min(np.amax(non_zero_x) + 1, image.shape[1])
        min_y = np.amin(non_zero_y)
        max_y = min(np.amax(non_zero_y) + 1, image.shape[0])

        return image[min_y:max_y, min_x:max_x]

    def from_file(self, path):
        image = Image.open(path)
        return self.from_image(image)

    def from_image(self, image):
        hog_val = self.features(image)
        if hog_val is None:
            return ""
        nbr = self.clf.predict(np.array([hog_val], 'float32'))

        return str(int(nbr[0]))

    def features_from_file(self, path):
        image = Image.open(path)
        return self.features(image)

    def features(self, image):
        self.load_classifier()

        image = image.convert('RGBA')
        open_cv_image = np.array(image)
        # debug_save_image(open_cv_image, "initial")

        im = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        im = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

        im = self.filter_big_blobs(im)
        if im is None:
            return None

        im = self.trim_image(im)

        # debug_save_image(im, "before-resize")

        im = cv2.resize(im.copy(), (28, 28))

        # debug_save_image(im, "resized")
        return hog(im, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)

    def tesseract_from_file(self, path):
        return self.tesseract_from_image(Image.open(path))

    def tesseract_from_image(self, image):
        # debug_save_image(np.array(image), "non-handwritten")
        read = pytesseract.image_to_string(image, config="-psm 10 {}".format(self.__TESSERACT_CONFIG))
        if read:
            return str(read[0])
        return ""
