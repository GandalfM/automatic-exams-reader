from PyQt5.QtGui import QPixmap

from aer.domain.template import Template
from aer.image.drawing import Drawing


class TemplateViewController:
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.ui = mainwindow.ui

        self.drawing = Drawing()
        self._selectedtemplate = None
        self._default_exam = None

    @property
    def selectedtemplate(self):
        return self._selectedtemplate

    @selectedtemplate.setter
    def selectedtemplate(self, filename):
        file = open(filename, "r")

        self._selectedtemplate = Template.from_file(file)
        content = self._selectedtemplate.to_json()
        self.ui.templateTextEdit.setText(content)
        self._draw_template()

    @property
    def default_exam(self):
        return self._default_exam

    @default_exam.setter
    def default_exam(self, exam):
        self._default_exam = exam
        self._draw_template()

    def _draw_template(self):
        image = self._default_exam
        if self._selectedtemplate is not None:
            image = self.drawing.draw_template(self._default_exam, self._selectedtemplate)
        self.ui.templateViewLabel.setPixmap(QPixmap.fromImage(image))

