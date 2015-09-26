from aer.domain.template import Template


class TemplateFile:

    def __init__(self, filename, size=None):
        self._file = None
        self.changed = False

        if filename != "":
            self._file = open(filename, "r+")
            self._template = Template.from_file(self.file)
        else:
            if size is None:
                size = (1000, 750)
            self._template = Template("name", size)

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, value):
        if self._template != value:
            self._template = value
            self.changed = True

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, value):
        if not self._file.closed:
            self._file.close()
        self._file = value
