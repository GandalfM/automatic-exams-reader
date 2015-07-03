from PyQt5.QtWidgets import QFileDialog

class MenuController:

    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.ui = mainwindow.ui

        self.ui.actionTemplateOpen.triggered.connect(self.on_template_open_triggered)
        self.ui.actionExamsImport.triggered.connect(self.on_exam_open_triggered)

    def on_template_open_triggered(self):
        files = QFileDialog.getOpenFileNames(self.mainwindow, "Open template")
        filtered = [x for x in files[0] if x.endswith(".template")]
        self.mainwindow.template_list_controller.templates = filtered
        self.ui.statusbar.showMessage("Loaded {} templates".format(len(filtered)))

    def on_exam_open_triggered(self):
        files = QFileDialog.getOpenFileNames(self.mainwindow, "Import exams")
        filtered = [x for x in files[0] if x.endswith(".jpg")]
        self.mainwindow.examcontroller.exams = filtered
        self.ui.statusbar.showMessage("Loaded {} exams".format(len(filtered)))
