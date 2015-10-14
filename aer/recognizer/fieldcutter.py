from PIL import Image
import numpy as np

import cv2


class FieldCutter:
    def __init__(self):
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.thickness = 5
        self.thickness = 5
        self.area_coeff = 0.75
        self.thresh_value = 200
        self.connectivity = 4
        self.delta = 10

    def cut_field(self, field):
        # create black and white image
        img = np.array(field)
        mat = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, mat = cv2.threshold(mat, self.thresh_value, 255, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        mat = cv2.morphologyEx(mat, cv2.MORPH_OPEN, kernel)
        # find all blobs and label them
        n, labels, stats, _ = cv2.connectedComponentsWithStats(mat, self.connectivity)
        # find the biggest blob area (we assume 'background' is not the biggest blob
        tmp = np.argwhere(stats[1:, 4] == max(stats[1:, 4]))
        index = (tmp[0][0] + 1, 4)
        max_area = stats[index]
        fields = []
        for i in range(1, n):
            # get rid of too small blobs or being in another shape e.g. [______] and []
            if stats[i, 4] < max_area * self.area_coeff or not self.has_similar_shape(stats[i], stats[index[0]]):
                continue
            # create mask
            mask = np.zeros(mat.shape, np.uint8)
            mask.fill(0)
            result = np.empty(img.shape, img.dtype)
            result.fill(255)
            idx = (labels == i)
            mask[idx] = 255
            _, contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(mask, contours, -1, self.white, cv2.FILLED)
            cv2.drawContours(mask, contours, -1, self.black, self.thickness)
            idx = (mask != 0)
            # copy colored image
            result[idx] = img[idx]
            rect = cv2.boundingRect(contours[0])
            # crop the image
            digit = result[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]]
            fields.append(Image.fromarray(digit))

        return fields

    def has_similar_shape(self, rect1, rect2):
        return abs(rect1[2] - rect2[2]) < self.delta and abs(rect1[3] - rect2[3]) < self.delta
