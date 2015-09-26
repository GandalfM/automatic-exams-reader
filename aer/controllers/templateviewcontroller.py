from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui

from aer.domain.template import Template
from aer.domain.templatefile import TemplateFile
from aer.image.drawing import Drawing


class TemplateViewController:

    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.ui = mainwindow.ui

        self.ui.templateTextEdit.textChanged.connect(self.template_text_changed)

        self.drawing = Drawing()
        self._default_exam = None
        self._selected_template = None
        self._scale = 1.0

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        self._draw_template()

    @property
    def selected_template(self):
        return self._selected_template

    @selected_template.setter
    def selected_template(self, filename):
        size = None
        if self._default_exam is not None:
            size = (self._default_exam.width(), self._default_exam.height())
        self._selected_template = TemplateFile(filename, size)
        content = self._selected_template.template.to_json()
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
        if self._selected_template is not None:
            image = self.drawing.draw_template(self._default_exam, self._selected_template.template, self._scale)
        else:
            image = self.drawing.resize(self._default_exam, self._scale)
        self.ui.templateViewLabel.setPixmap(QPixmap.fromImage(image))

    def template_text_changed(self):
        data = self.ui.templateTextEdit.toPlainText()
        try:
            template = Template.from_json(data)
            self._selected_template.template = template
            color = QtGui.QColor("white")
        except (ValueError, Exception):
            color = QtGui.QColor("#ff9999")
        palette = self.ui.templateTextEdit.palette()
        palette.setColor(QtGui.QPalette.Base, color)
        self.ui.templateTextEdit.setPalette(palette)
