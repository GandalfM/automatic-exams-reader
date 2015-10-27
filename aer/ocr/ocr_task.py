from PyQt5.QtCore import QThread, pyqtSignal
from aer.ocr.ocr import *
from aer.recognizer.recognizer import Recognizer
from aer.domain.templatefile import TemplateFile


class OcrTask(QThread):
    finished = pyqtSignal()
    ocr = Ocr()

    def __init__(self):
        super().__init__()
        self.exams = []
        self.template = None

    def _process_exam(self, exam, recognizer):
        result = recognizer.recognize_from_path(exam)
        print(result)

    def run(self):
        if not self.template:
            self.finished.emit()
            return

        template = self.template
        recognizer = Recognizer(template)

        for exam in self.exams:
            self._process_exam(exam, recognizer)

        self.finished.emit()