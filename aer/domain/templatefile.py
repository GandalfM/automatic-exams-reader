from aer.domain.template import Template


class TemplateFile:

    def __init__(self, filename):
        super().__init__()
        self.file = open(filename, "r+")
        self._template = Template.from_file(self.file)
        self.changed = False

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, value):
        if self._template != value:
            self._template = value
            self.changed = True
