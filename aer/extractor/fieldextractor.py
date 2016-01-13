from aer.domain.field import FieldType
from aer.domain.mark import Mark
from aer.utils.utils import combine


def convert_template_rect_to_crop_rect(template_rect):
    x, y, w, h = template_rect
    return x, y, x + w, y + h


def extract_function_factory(exam_image):
    def extract_function(field):
        combined_function = combine(convert_template_rect_to_crop_rect, exam_image.crop)
        if isinstance(field, list):
            return list(map(combined_function, field))
        return combined_function(field)
    return extract_function


class FieldExtractor:
    def __init__(self, template):
        self.template = template

    def extract_fields_from_exam(self, exam_image):
        extract_function = extract_function_factory(exam_image)
        for field in filter(lambda field: field.field_type != FieldType.MARK, self.template.get_fields().values()):
            field.image = extract_function(field.rect)
            yield field

    def extract_mark_from_exam(self, exam_image):
        extract_function = extract_function_factory(exam_image)
        if not self.template.type_exists(FieldType.MARK):
            return None

        extracted_field = extract_function(self.template.get_fields_with_type(FieldType.MARK)[0].rect)
        mark = Mark()
        mark.image = extracted_field
        mark.place = self.template.get_fields_with_type(FieldType.MARK)[0].rect[:2]
        return mark
