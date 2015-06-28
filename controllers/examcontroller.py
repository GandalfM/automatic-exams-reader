from PyQt5.QtCore import QStringListModel
from PyQt5.QtGui import QImage, QPixmap


class ExamController:
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.ui = mainwindow.ui

        self._exams = []
        self._selected_exam = None

        self.ui.examListView.clicked.connect(self.on_exam_text_selection)

    def on_exam_text_selection(self, index):
        self.selected_exam = self._exams[index.row()]

    @property
    def selected_exam(self):
        return self._selected_exam

    @selected_exam.setter
    def selected_exam(self, value):
        if self._selected_exam != value:
            self._selected_exam = value
            image = QImage(value)
            self.ui.imageLabel.setPixmap(QPixmap.fromImage(image))

    @property
    def exams(self):
        return self._exams

    @exams.setter
    def exams(self, value):
        self._exams = value
        model = QStringListModel(map(lambda x: str(x), value))
        self.ui.examListView.setModel(model)
