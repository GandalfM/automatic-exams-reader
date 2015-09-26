from PyQt5.QtWidgets import QFileDialog

class MenuController:

    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.ui = mainwindow.ui
        self.template_dialog_path = "."
        self.exam_dialog_path = "."

        self.ui.actionTemplateOpen.triggered.connect(self.on_template_open_triggered)
        self.ui.actionExamsImport.triggered.connect(self.on_exam_open_triggered)
        self.ui.actionTemplateSave.triggered.connect(self.on_template_save)
        self.ui.actionTemplateSaveAs.triggered.connect(self.on_template_save_as)

    def on_template_open_triggered(self):
        files = QFileDialog.getOpenFileNames(self.mainwindow, "Open template", self.template_dialog_path)
        filtered = [x for x in files[0] if x.lower().endswith(".template")]
        if len(filtered) > 0:
            self.template_dialog_path = filtered[0]
        self.mainwindow.template_list_controller.templates = filtered
        self.ui.statusbar.showMessage("Loaded {} templates".format(len(filtered)))

    def on_exam_open_triggered(self):
        files = QFileDialog.getOpenFileNames(self.mainwindow, "Import exams", self.exam_dialog_path)
        filtered = [x for x in files[0] if x.lower().endswith(".jpg")]
        if len(filtered) > 0:
            self.exam_dialog_path = filtered[0]
        self.mainwindow.examcontroller.exams = filtered
        self.ui.statusbar.showMessage("Loaded {} exams".format(len(filtered)))

    def on_template_save(self):
        template_file = self.mainwindow.template_view_controller.selected_template
        if template_file is not None:
            if template_file.changed:
                self.save_file(template_file.file, template_file.template)
                template_file.changed = False
            else:
                self.ui.statusbar.showMessage("Template contains errors or no changes from last save.".format(template_file.file.name))

    def on_template_save_as(self):
        template_file = self.mainwindow.template_view_controller.selected_template
        if template_file is not None:
            filename = QFileDialog.getSaveFileName(self.mainwindow, "Save template", self.template_dialog_path)[0]
            if filename.split(".")[-1] != "template":
                filename += ".template"
            file = open(filename, "w")
            self.save_file(file, template_file.template)
            file.close()

    def save_file(self, file, template):
        file.seek(0)
        file.write(template.to_json())
        file.truncate()
        self.ui.statusbar.showMessage("{} saved successfully.".format(file.name))
