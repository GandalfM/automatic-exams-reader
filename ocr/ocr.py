from PIL import Image
from PIL import ImageEnhance
from sklearn.externals import joblib
from sklearn import datasets
from skimage.feature import hog
from sklearn.svm import LinearSVC
import numpy as np
import os

class Ocr:
    __CLASSIFIER_FILE = "cls.pkl"
    __TO_WHITE_BLACK_THRESHOLD = 180

    def __init__(self):
        self.clf = None

    def create_classifier(self):
        # source: http://hanzratech.in/2015/02/24/handwritten-digit-recognition-using-opencv-sklearn-and-python.html
        dataset = datasets.fetch_mldata("MNIST Original")
        features = np.array(dataset.data, 'int16')
        labels = np.array(dataset.target, 'int')

        list_hog_fd = []
        for feature in features:
            #Image.fromarray(feature.reshape((28,28))).save("feature.jpg", "JPEG")
#            print(feature.reshape((28, 28)))
#            print("next")
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

    def from_file(self, path):
        image = Image.open(path)
        return self.from_image(image)

    def from_image(self, image):
        self.load_classifier()
        image = ImageEnhance.Color(image).enhance(0.0)
        image = ImageEnhance.Contrast(image).enhance(2.0)
        image = image.convert('L')
        image = image.resize((28, 28), Image.ANTIALIAS)
        #image.point(lambda x: 0 if x < self.__TO_WHITE_BLACK_THRESHOLD else 255, 'L')

        image.save("test.bmp", "BMP")
        image_data = np.asmatrix(image, "int16")
        print (image_data)

        roi_hog_fd = hog(image_data, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
        nbr = self.clf.predict(np.array([roi_hog_fd], 'float64'))
        return int(nbr[0])
