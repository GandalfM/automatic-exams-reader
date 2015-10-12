import os

from PIL import Image
from sklearn.externals import joblib
from sklearn import datasets
from skimage.feature import hog
from sklearn.svm import LinearSVC
import numpy as np

import cv2


class Ocr:
    __CLASSIFIER_FILE = "cls.pkl"
    __TO_WHITE_BLACK_THRESHOLD = 100

    def __init__(self):
        self.clf = None
        self._debug_image_iterator = 0

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

    def _debug_save_image(self, image):
        cv2.imwrite("image" + str(self._debug_image_iterator) + ".jpg", image)
        self._debug_image_iterator += 1

    def filter_biggest_blob(self, image):
        im2, contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        maxContour = contours[0]
        for contour in contours:
            if cv2.contourArea(maxContour) < cv2.contourArea(contour):
                maxContour = contour

        image.fill(0)
        cv2.drawContours(image, [maxContour], -1, 255, -1)

    def from_image(self, image, roi=None):
        self.load_classifier()

        image = image.convert('RGB')
        open_cv_image = np.array(image)

        if roi:
            x = int(roi[0])
            y = int(roi[1])
            width = int(roi[2])
            height = int(roi[3])
            open_cv_image = open_cv_image[y:y+height, x: x + width]

        im_gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        cv2.equalizeHist(im_gray, im_gray)
        im_gray = cv2.medianBlur(im_gray, 5)
        ret, im_th = cv2.threshold(im_gray, self.__TO_WHITE_BLACK_THRESHOLD, 255, cv2.THRESH_BINARY_INV)
        self.filter_biggest_blob(im_th)
        roi = cv2.resize(im_th.copy(), (28, 28), interpolation=cv2.INTER_AREA)
        roi = cv2.erode(roi, (3, 3))

        roi_hog_fd = hog(roi, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
        nbr = self.clf.predict(np.array([roi_hog_fd], 'float64'))
        return int(nbr[0])
