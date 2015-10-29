import os
from PIL import Image

from PyQt5.QtCore import QStringListModel

from aer.config.configconstants import *
from aer.image.drawing import Drawing
from aer.utils.imageutil import pil2pixmap


class ExamController:
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.ui = mainwindow.ui
        self.config = self.mainwindow.config_manager

        self.template_view_controller = mainwindow.template_view_controller
        self.ui.examViewLabel.wheelScrolled.connect(self.on_wheel_scroll)

        exams = self.config.get_property(EXAMS_LOADED, [])
        for ex in exams:
            if not os.path.exists(ex):
                exams.remove(ex)

        self.exams = exams
        self._selected_exam = None
        self._scale = self.config.get_property(EXAM_IMAGE_ZOOM, 1.0)
        self.drawing = Drawing()
        self.ui.examListView.clicked.connect(self.on_exam_text_selection)

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        self.config.set_property(EXAM_IMAGE_ZOOM, self._scale)
        self._draw_exam()

    def on_exam_text_selection(self, index):
        self.selected_exam = self._exams[index.row()]

    @property
    def selected_exam(self):
        return self._selected_exam

    @selected_exam.setter
    def selected_exam(self, value):
        image = Image.open(value)
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
            image = Image.open(self._exams[0])
            self.template_view_controller.default_exam = image
        self.config.set_property(EXAMS_LOADED, value)

    def _draw_exam(self):
        image = self.drawing.resize(self._selected_exam, self._scale)
        self.ui.examViewLabel.setPixmap(pil2pixmap(image))

    def on_wheel_scroll(self, event):
        if self.selected_exam is not None:
            delta = event.angleDelta().y()
            if delta > 0 and self.scale <= 2.0:
                self.scale += 0.1
            if delta < 0 and self.scale >= 0.2:
                self.scale -= 0.1
