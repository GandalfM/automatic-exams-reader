import json
from domain.serialization import TemplateEncoder

class Template:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self._fields = {}

    def add_field(self, name, rect):
        if name in self._fields:
            raise Exception("You already have a field with such a name.")
        if len(rect) != 4:
            raise Exception("The rect parameter must be an iterable of size 4.")
        if rect[0] + rect[2] > self.size[0] or rect[1] + rect[3] > self.size[1]:
            raise Exception("The given rectangle does not fit.")
        self._fields[name] = rect

    def get_fields(self):
        return self._fields

    def get_field_rects(self):
        return self._fields.values()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.to_json()

    def to_json(self):
        return json.dumps(self, cls=TemplateEncoder)

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
    def from_file(file):
        content = file.read()
        return Template.from_json(content)
