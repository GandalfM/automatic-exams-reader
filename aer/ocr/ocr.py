from PIL import Image
from sklearn.externals import joblib
from sklearn import datasets
from skimage.feature import hog
from sklearn.svm import LinearSVC
import numpy as np
from aer.utils.imageutil import *

import cv2


class Ocr:
    __CLASSIFIER_FILE_NAME = "cls.pkl"
    __TO_WHITE_BLACK_THRESHOLD = 100

    def __init__(self):
        self.clf = None
        parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.__CLASSIFIER_FILE = os.path.join(parent_dir, self.__CLASSIFIER_FILE_NAME)
        self.connectivity = 4

    def create_classifier(self):
        # source: http://hanzratech.in/2015/02/24/handwritten-digit-recognition-using-opencv-sklearn-and-python.html
        dataset = datasets.fetch_mldata("MNIST Original")
        features = np.array(dataset.data, 'int16')
        labels = np.array(dataset.target, 'int')

        list_hog_fd = []
        for feature in features:
            fd = hog(feature.reshape((28, 28)), orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
            list_hog_fd.append(fd)
        hog_features = np.array(list_hog_fd, 'float64')
        self.clf = LinearSVC()
        self.clf.fit(hog_features, labels)
        joblib.dump(self.clf, self.__CLASSIFIER_FILE, compress=3)

    def load_classifier(self):
        if not os.path.isfile(self.__CLASSIFIER_FILE):
            self.create_classifier()
        else:
            self.clf = joblib.load(self.__CLASSIFIER_FILE)

    def from_file(self, path, roi=None):
        image = Image.open(path)
        return self.from_image(image, roi)

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

    def from_image(self, image, roi=None):
        self.load_classifier()

        image = image.convert('RGBA')
        open_cv_image = np.array(image)
        # debug_save_image(open_cv_image, "initial")

        if roi:
            x = int(roi[0])
            y = int(roi[1])
            width = int(roi[2])
            height = int(roi[3])
            open_cv_image = open_cv_image[y:y+height, x: x + width]

        im_gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        canny_image = cv2.Canny(im_gray, 70, 255)
        # debug_save_image(canny_image, "first-canny")

        canny_image = cv2.dilate(canny_image, kernel_ellipse(3))
        canny_image = cv2.morphologyEx(canny_image, cv2.MORPH_CLOSE, kernel_ellipse(5))

        # debug_save_image(canny_image, "canny")
        canny_image = self.filter_biggest_blob(canny_image)
        # debug_save_image(canny_image, "canny-biggest")

        roi = cv2.resize(canny_image.copy(), (28, 28))
        # debug_save_image(roi, "small")
        roi_hog_fd = hog(roi, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
        nbr = self.clf.predict(np.array([roi_hog_fd], 'float64'))
        return int(nbr[0])
