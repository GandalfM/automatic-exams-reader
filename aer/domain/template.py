import json

from PyQt5.QtCore import QObject, pyqtSignal
from aer.domain.reporttemplatebuilder import ReportTemplateBuilder

from aer.domain.serialization import TemplateEncoder


class Template(QObject):

    templateChanged = pyqtSignal()

    def __init__(self, name, size):
        super().__init__()
        self.name = name
        self.size = size
        self._fields = {}

    def add_field(self, name, rect, emit=True):
        if name in self._fields:
            raise Exception("Already have a field with name " + name)
        if len(rect) != 4:
            raise Exception("The rect parameter must be an iterable of size 4.")
        if rect[0] + rect[2] > self.size[0] or rect[1] + rect[3] > self.size[1]:
            raise Exception("The given rectangle does not fit.")

        self._fields[name] = rect
        if emit:
            self.templateChanged.emit()

    def field_exists(self, name):
        return name in self._fields

    def report_builder(self):
        return ReportTemplateBuilder(self)

    def get_fields(self):
        return self._fields

    def get_field_at(self, x, y):
        for key, rect in self._fields.items():
            if Template._point_inside_rect(rect, x, y):
                return key, rect
        return None

    def move_field_to(self, key, new_x, new_y):
        if key in self._fields:
            x, y, w, h = self._fields[key]
            self._fields[key] = [new_x, new_y, w, h]
            self.templateChanged.emit()
            return self._fields[key]

    def remove_field_at(self, x, y):
        result = self.get_field_at(x, y)
        if result:
            del self._fields[result[0]]
            self.templateChanged.emit()
            return result


    @staticmethod
    def _point_inside_rect(rect, x, y):
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
            template.add_field(field[0], tuple(field[1]))
        return template

    @staticmethod
    def from_json_no_event(s):
        d = json.loads(s)
        template = Template(d["name"], tuple(d["size"]))
        for field in d["rects"]:
            template.add_field(field[0], tuple(field[1]), False)
        return template

    @staticmethod
    def from_file(file):
        content = file.read()
        return Template.from_json(content)
