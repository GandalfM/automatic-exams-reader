from aer.extractor.FieldExtractor import FieldExtractor
from aer.ocr.ocr import Ocr
from aer.recognizer.FieldCutter import FieldCutter

__author__ = 'Bartek'

class Recognizer:
    def __init__(self, template):
        self.template = template
        self.extractor = FieldExtractor(template)
        self.field_cutter = FieldCutter()
        self.ocr = Ocr()
        self.ocr.load_classifier()

    def recognize(self, exam_image):
        extracted_fields = self.extractor.extract_fields_from_exam(exam_image)
        for extracted_field in extracted_fields:
            single_character_images = self.field_cutter.cut_field(extracted_field)
            recognized_str = ''.join([str(self.ocr.from_image(char)) for char in single_character_images])

    def cut_field_into_single_characters(self, field):
        return field
