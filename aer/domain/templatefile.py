from PyQt5.QtCore import pyqtSignal, QObject
from aer.domain.template import Template


class TemplateFile(QObject):
    
    changedStatus = pyqtSignal()

    def __init__(self, filename, size=None):
        super().__init__()
        self._file = None
        self._changed = False

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
        if self._file is not None and not self._file.closed:
            self._file.close()
        self._file = value

    @property
    def changed(self):
        return self._changed

    @changed.setter
    def changed(self, value):
        self._changed = value
        self.changedStatus.emit()
