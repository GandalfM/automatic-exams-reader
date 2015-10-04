from PyQt5.QtCore import QStringListModel
from PyQt5.QtGui import QImage, QPixmap

from aer.config.configconstants import *
from aer.image.drawing import Drawing


class ExamController:
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.ui = mainwindow.ui
        self.config = self.mainwindow.config_manager

        self.template_view_controller = mainwindow.template_view_controller
        self.ui.examViewLabel.wheelScrolled.connect(self.on_wheel_scroll)

        self.exams = self.config.get_property(EXAMS_LOADED, [])
        self._selected_exam = None
        self._scale = 1.0
        self.drawing = Drawing()
        self.ui.examListView.clicked.connect(self.on_exam_text_selection)

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        self._draw_exam()

    def on_exam_text_selection(self, index):
        self.selected_exam = self._exams[index.row()]

    @property
    def selected_exam(self):
        return self._selected_exam

    @selected_exam.setter
    def selected_exam(self, value):
        image = QImage(value)
        if self._selected_exam != image:
            self._selected_exam = image
            self.template_view_controller.default_exam = image
            self._draw_exam()

    @property
    def exams(self):
        return self._exams

    @exams.setter
    def exams(self, value):
        self._exams = value
        model = QStringListModel(map(lambda x: str(x), value))
        self.ui.examListView.setModel(model)
        if self._exams:
            image = QImage(self._exams[0])
            self.template_view_controller.default_exam = image
        self.config.set_property(EXAMS_LOADED, value)

    def _draw_exam(self):
        image = self.drawing.resize(self._selected_exam, self._scale)
        self.ui.examViewLabel.setPixmap(QPixmap.fromImage(image))

    def on_wheel_scroll(self, event):
        if self.selected_exam is not None:
            delta = event.angleDelta().y()
            if delta > 0 and self.scale <= 2.0:
                self.scale += 0.1
            if delta < 0 and self.scale >= 0.2:
                self.scale -= 0.1
