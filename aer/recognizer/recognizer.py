import numpy as np
from PIL import Image

from aer.extractor.fieldextractor import FieldExtractor
from aer.ocr.ocr import Ocr
from aer.recognizer.fieldcutter import FieldCutter
from aer.domain.field import FieldType
import cv2


class Recognizer:
    def __init__(self, template):
        self.template = template
        self.extractor = FieldExtractor(template)
        self.field_cutter = FieldCutter()
        self.ocr = Ocr()
        self.ocr.load_classifier()

    def recognize_from_path(self, path, mark):
        image = Image.open(path)
        if mark is not None:
            image = self.translate_image(image, mark)
        return self.recognize(image)

    def recognize(self, exam_image):
        extracted_fields = self.extractor.extract_fields_from_exam(exam_image)
        result = {}
        for field_obj in extracted_fields:
            single_character_images = self.field_cutter.cut_field(field_obj.image)
            field = []
            for row in single_character_images:
                recognized_str = ""
                if field_obj.field_type == FieldType.HANDWRITTEN:
                    recognized_str = ''.join([str(self.ocr.from_image(char)) for char in row])
                elif field_obj.field_type == FieldType.PRINTED:
                    recognized_str = ''.join([str(self.ocr.tesseract_from_image(char)) for char in row])
                field.append(recognized_str)
            result[field_obj.name] = field
        return result

    def translate_image(self, image, mark):
        mat = np.array(image)
        temp = np.array(mark.image)
        res = cv2.matchTemplate(mat, temp, cv2.TM_CCOEFF_NORMED)
        minmax = cv2.minMaxLoc(res)
        rows, cols, _ = mat.shape
        vector = (mark.place[0] - minmax[3][0], mark.place[1] - minmax[3][1])

        m = np.float32([[1, 0, vector[0]], [0, 1, vector[1]]])
        dst = cv2.warpAffine(mat, m, (cols, rows))
        return Image.fromarray(dst)
