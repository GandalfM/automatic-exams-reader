from aer.utils.utils import combine

__author__ = 'Bartek'


def convert_template_rect_to_crop_rect(template_rect):
    x, y, w, h = template_rect
    return x, y, x + w, y + h


def extract_function_factory(exam_image):
    def extract_function(field):
        combined_function = combine(convert_template_rect_to_crop_rect, exam_image.crop)
        if isinstance(field, list):
            return list(map(combined_function, field))
        return exam_image.crop(combined_function(field))

    return extract_function


class FieldExtractor:
    def __init__(self, template):
        self.template = template

    def extract_fields_from_exam(self, exam_image):
        extract_function = extract_function_factory(exam_image)
        extracted_fields = {k: extract_function(v) for k, v in self.template.get_fields().items()}
        return extracted_fields
