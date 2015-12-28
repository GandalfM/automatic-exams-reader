from enum import Enum


class FieldType(Enum):
    MARK = 1
    HANDWRITTEN = 2
    PRINTED = 3


class Field:

    def __init__(self, rect=None, name="default", field_type=FieldType.HANDWRITTEN):
        self.rect = rect
        self.name = name
        self.field_type = field_type

    def to_dict(self):
        return {
            "rect": self.rect,
            "name": self.name,
            "field_type": self.field_type.value
        }

    def __eq__(self, other):
        if isinstance(other, Field):
            return self.to_dict() == other.to_dict()
        return False

    @staticmethod
    def add_to_template(template, data):
        if "field_type" in data:
            template.add_field(data["name"], rect=data["rect"], field_type=FieldType(data["field_type"]))
        else:
            template.add_field(data["name"], rect=data["rect"])
