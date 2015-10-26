from aer.extractor.fieldextractor import FieldExtractor
from aer.ocr.ocr import Ocr
from aer.recognizer.fieldcutter import FieldCutter
from PIL import Image

class Recognizer:
    def __init__(self, template):
        self.template = template
        self.extractor = FieldExtractor(template)
        self.field_cutter = FieldCutter()
        self.ocr = Ocr()
        self.ocr.load_classifier()

    def recognize_from_path(self, path):
        image = Image.open(path)
        return self.recognize(image)

    def recognize(self, exam_image):
        extracted_fields = self.extractor.extract_fields_from_exam(exam_image)
        result = {}
        for field_name, field_image in extracted_fields.items():
            single_character_images = self.field_cutter.cut_field(field_image)
            field = []
            for row in single_character_images:
                recognized_str = ''.join([str(self.ocr.from_image(char)) for char in row])
                field.append(recognized_str)
            result[field_name] = field
        return result
