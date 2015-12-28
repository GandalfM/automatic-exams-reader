import json

from PyQt5.QtCore import QObject, pyqtSignal
from aer.domain.reporttemplatebuilder import ReportTemplateBuilder
from aer.domain.field import Field

from aer.domain.serialization import TemplateEncoder


class Template(QObject):

    templateChanged = pyqtSignal()

    def __init__(self, name, size):
        super().__init__()
        self.name = name
        self.size = size
        self._fields = {}

    def add_field(self, name, rect, emit=True):
        rect = self._normalize_rect(rect)

        if self.field_exists(name):
            raise Exception("Already have a field with name " + name)
        if len(rect) != 4:
            raise Exception("The rect parameter must be an iterable of size 4.")
        if rect[0] + rect[2] > self.size[0] or rect[1] + rect[3] > self.size[1]:
            raise Exception("The given rectangle does not fit.")

        field = Field(name=name, rect=rect)
        self._fields[name] = field
        if emit:
            self.templateChanged.emit()

    def _normalize_rect(self, rect):
        x, y, w, h = rect
        if w < 0:
            x += w
            w = abs(w)
        if h < 0:
            y += h
            h = abs(h)
        return x, y, w, h

    def field_exists(self, name):
        return name in self._fields

    def report_builder(self):
        return ReportTemplateBuilder(self)

    def get_fields(self):
        return self._fields

    def get_field(self, key):
        return self._fields[key]

    def get_field_at(self, x, y):
        for key, field in self._fields.items():
            if Template._point_inside_rect(field, x, y):
                return field
        return None

    def move_field_to(self, key, new_x, new_y):
        if self.field_exists(key):
            field = self.get_field(key)
            x, y, w, h = field.rect
            field.rect = [new_x, new_y, w, h]
            self.templateChanged.emit()
            return field

    def scale_field(self, key, new_w, new_h):
        if self.field_exists(key):
            field = self.get_field(key)
            x, y, w, h = field.rect
            field.rect = [x, y, new_w, new_h]
            self.templateChanged.emit()
            return field

    def remove_field_at(self, x, y):
        result = self.get_field_at(x, y)
        if result:
            del self._fields[result.name]
            self.templateChanged.emit()
            return result


    @staticmethod
    def _point_inside_rect(field, x, y):
        rect = field.rect
        return rect[0] < x < rect[0] + rect[2] and rect[1] < y < rect[1] + rect[3]

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.to_json()

    def to_json(self):
        return json.dumps(self, cls=TemplateEncoder, indent=4)

    def __eq__(self, other):
        if isinstance(other, Template):
            return (self.name == other.name) and (self.size == other.size) and (self._fields == other._fields)
        return False

    @staticmethod
    def from_json(s):
        d = json.loads(s)
        template = Template(d["name"], tuple(d["size"]))
        for field in d["rects"]:
            Field.add_to_template(template, field)
        return template

    @staticmethod
    def from_file(file):
        content = file.read()
        return Template.from_json(content)
