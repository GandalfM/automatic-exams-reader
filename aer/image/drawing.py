from PyQt5 import QtGui
import cv2
import numpy as np


class Drawing:

    def __init__(self):
        self._color = (255, 0, 0)
        self._thickness = 2
        self._font_type = cv2.FONT_HERSHEY_COMPLEX_SMALL
        self._font_size = 0.8
        self._text_margin = 10

    def _image_to_mat(self, image):
        image = image.convertToFormat(QtGui.QImage.Format_RGB888)

        width = image.width()
        height = image.height()

        ptr = image.bits()
        ptr.setsize(image.byteCount())
        mat = np.array(ptr).reshape(height, width, 3)
        return mat

    def _mat_to_image(self, mat):
        return QtGui.QImage(mat.data, mat.shape[1], mat.shape[0], QtGui.QImage.Format_RGB888)

    def draw_template(self, image, template):
        mat = self._image_to_mat(image)

        # resize image to template dimensions
        mat = cv2.resize(mat, template.size)

        # draw all rects
        for name, rects in template.get_fields().items():
            for rect in rects:
                cv2.rectangle(mat, rect[:2], (rect[0] + rect[2], rect[1] + rect[3]), self._color, self._thickness)
                text_pos = (rect[0] + self._text_margin, rect[1] + rect[3] - self._text_margin)
                cv2.putText(mat, name, text_pos, self._font_type, self._font_size, self._color)

        return self._mat_to_image(mat)
