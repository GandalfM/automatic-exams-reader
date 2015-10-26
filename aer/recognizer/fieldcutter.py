from PIL import Image
import numpy as np
from aer.utils.imageutil import debug_save_image

import cv2


class FieldCutter:
    def __init__(self):
        # self.white = (255, 255, 255)
        self.white = 255
        # self.black = (0, 0, 0)
        self.black = 0
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
            rect = cv2.boundingRect(contours[0])
            # crop the image
            # let's assume that border will take 2,5% of each dimension
            width_border_insurance = rect[3] * 0.025
            height_border_insurance = rect[2] * 0.025
            digit = img[rect[1] + width_border_insurance:rect[1] + rect[3] - width_border_insurance,
                    rect[0] + height_border_insurance: rect[0] + rect[2] - height_border_insurance]

            # it's the first image
            fields.append((rect, Image.fromarray(digit)))

        return self._sort_fields(fields)

    def _sort_fields(self, fields):
        """
        Sort fields.
        Return fields sorted in rows

        :param fields: list
        :return:
        """
        if not fields:
            return []

        average_height = sum(map(lambda field: field[0][2], fields)) / len(fields)

        sorted_by_y = sorted(fields, key=lambda field: field[0][1])

        array_fields = []
        row = []
        y = sorted_by_y[0][0][1]

        for field in sorted_by_y:
            if field[0][1] > y + average_height / 2:
                array_fields.append(row)
                row = [field]
                y = field[0][1]
            else:
                row.append(field)

        array_fields.append(row)

        result = []
        for row in array_fields:
            row.sort(key=lambda field: field[0][0])
            result.append(list(map(lambda field: field[1], row)))
        return result

    def has_similar_shape(self, rect1, rect2):
        return abs(rect1[2] - rect2[2]) < self.delta and abs(rect1[3] - rect2[3]) < self.delta
