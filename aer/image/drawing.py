from PIL import Image
from PIL.ImageDraw import ImageDraw
from PIL.ImageDraw import Draw
import numpy as np

import cv2


class Drawing:
    def __init__(self, base_img, scale):
        self._color = (255, 0, 0)
        self._tmp_color = (0, 0, 255)
        self._thickness = 3
        self._font_type = cv2.FONT_HERSHEY_COMPLEX_SMALL
        self._font_size = 1.5
        self._text_margin = 10

        if base_img:
            new_size = [int(x * scale) for x in base_img.size]
            self.base_img = base_img.copy().resize(new_size)
            self.canvas = self.base_img.copy()
        self.scale = scale

    def _draw_rect(self, dr, rect, width=4):
        x1, y1, w, h = rect
        x2, y2 = x1 + w, y1 + h
        for r in range(0, width):
            dr.rectangle([x1 + r, y1 + r, x2 - r, y2 - r], outline="green")

    def _transformed_rect(self, rect):
        return [x * self.scale for x in rect]

    def draw_template(self, template, tmp_rect):
        draw = Draw(self.canvas)
        self.canvas.paste(self.base_img)
        for name, rect in template.get_fields().items():
            self._draw_rect(draw, self._transformed_rect(rect))

        if tmp_rect is not None:
            self._draw_rect(draw, self._transformed_rect(tmp_rect))
        # mat = np.array(image)
        #
        # # draw all rects
        # for name, rect in template.get_fields().items():
        #     cv2.rectangle(mat, rect[:2], (rect[0] + rect[2], rect[1] + rect[3]), self._color, self._thickness)
        #     text_pos = (rect[0] + self._text_margin, rect[1] + rect[3] - self._text_margin)
        #     cv2.putText(mat, name, text_pos, self._font_type, self._font_size, self._color)
        #
        # # draw temp rect
        # if tmp_rect is not None:
        #     cv2.rectangle(mat, tmp_rect[:2], (tmp_rect[0] + tmp_rect[2], tmp_rect[1] + tmp_rect[3]), self._tmp_color, self._thickness)
        #
        # # resize image to template dimensions
        # mat = cv2.resize(mat, None, None, self.scale, self.scale)
        # return Image.fromarray(mat)
        return self.canvas

    def resize(self, image, scale):
        mat = np.array(image)
        mat = cv2.resize(mat, None, None, scale, scale)
        return Image.fromarray(mat)

