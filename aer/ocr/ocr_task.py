from PyQt5.QtCore import QThread, pyqtSignal
from aer.ocr.ocr import *
from aer.domain.template import Template
from aer.domain.templatefile import TemplateFile
from time import sleep


class OcrTask(QThread):
    finished = pyqtSignal()
    ocr = Ocr()

    def __init__(self):
        super().__init__()
        self.exams = []
        self.template = None

    def _process_exam(self, exam):
        template_file = TemplateFile(self.template)
        template = template_file.template

        result = {}
        for name, fields in template.get_fields().items():
            results = []
            for roi in fields:
                results.append(self.ocr.from_file(exam, roi))
            result[name] = results

        print(result)

    def run(self):
        if not self.template:
            self.finished.emit()
            return

        for exam in self.exams:
            self._process_exam(exam)

        self.finished.emit()