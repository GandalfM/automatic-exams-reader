from PyQt5.QtWidgets import QFileDialog

class MenuController:

    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.ui = mainwindow.ui
        self.template_dialog_path = "."
        self.exam_dialog_path = "."

        self.ui.actionTemplateOpen.triggered.connect(self.on_template_open_triggered)
        self.ui.actionExamsImport.triggered.connect(self.on_exam_open_triggered)

    def on_template_open_triggered(self):
        files = QFileDialog.getOpenFileNames(self.mainwindow, "Open template", self.template_dialog_path)
        filtered = [x for x in files[0] if x.endswith(".template")]
        if len(filtered) > 0:
            self.template_dialog_path = filtered[0]
        self.mainwindow.template_list_controller.templates = filtered
        self.ui.statusbar.showMessage("Loaded {} templates".format(len(filtered)))

    def on_exam_open_triggered(self):
        files = QFileDialog.getOpenFileNames(self.mainwindow, "Import exams", self.exam_dialog_path)
        filtered = [x for x in files[0] if x.endswith(".jpg")]
        if len(filtered) > 0:
            self.exam_dialog_path = filtered[0]
        self.mainwindow.examcontroller.exams = filtered
        self.ui.statusbar.showMessage("Loaded {} exams".format(len(filtered)))
