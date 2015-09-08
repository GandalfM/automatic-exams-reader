from PyQt5.QtGui import QPixmap

from domain.template import Template


class TemplateViewController:
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.ui = mainwindow.ui

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

    @property
    def default_exam(self):
        return self._default_exam

    @default_exam.setter
    def default_exam(self, exam):
        self._default_exam = exam
        self.ui.templateViewLabel.setPixmap(QPixmap.fromImage(exam))
