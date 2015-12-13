from PyQt5.QtCore import QThread, pyqtSignal
from aer.ocr.ocr import *
from aer.recognizer.recognizer import Recognizer
import json
import pprint


class OcrTask(QThread):
    finished = pyqtSignal()
    ocr = Ocr()

    def __init__(self):
        super().__init__()
        self.exams = []
        self.template = None
        self.mark = None
        self.report_path = None
        self.pp = pprint.PrettyPrinter(indent=4)

    def _process_exam(self, exam, recognizer):
        return recognizer.recognize_from_path(exam, self.mark)

    def run(self):
        if not self.template:
            self.finished.emit()
            return

        template = self.template
        recognizer = Recognizer(template)

        results = []
        for exam in self.exams:
            result = self._process_exam(exam, recognizer)
            results.append({
                "result": result,
                "exam_path": exam
            })

        self.pp.pprint(results)

        with open(self.report_path, 'w') as outfile:
            json.dump(results, outfile, indent=1)

        self.finished.emit()
