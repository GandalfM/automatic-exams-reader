import os
from PyQt5.QtCore import QItemSelectionModel
from PyQt5.QtWidgets import QFileDialog
from aer.config.configconstants import *

class MenuController:

    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.config = self.mainwindow.config_manager
        self.ui = mainwindow.ui
        self.template_dialog_path = self.config.get_property(TEMPLATE_DIALOG_PATH_KEY, ".")
        self.exam_dialog_path = self.config.get_property(EXAM_DIALOG_PATH_KEY, ".")

        self.ui.actionTemplateOpen.triggered.connect(self.on_template_open_triggered)
        self.ui.actionExamsImport.triggered.connect(self.on_exam_open_triggered)
        self.ui.actionTemplateSave.triggered.connect(self.on_template_save)
        self.ui.actionTemplateSaveAs.triggered.connect(self.on_template_save_as)
        self.ui.actionTemplateNew.triggered.connect(self.on_template_new)

    def on_template_open_triggered(self):
        files, directories = QFileDialog.getOpenFileNames(self.mainwindow, "Open template", self.template_dialog_path)
        if files:
            self.config.set_property(TEMPLATE_DIALOG_PATH_KEY, os.path.dirname(files[0]))
            self.template_dialog_path = os.path.dirname(files[0])

        filtered = [x for x in files if x.lower().endswith(".template")]

        self.mainwindow.template_list_controller.templates = filtered
        self.config.set_property(TEMPLATES_LOADED, filtered)
        self.ui.statusbar.showMessage("Loaded {} templates".format(len(filtered)))

    def on_exam_open_triggered(self):
        files, directories = QFileDialog.getOpenFileNames(self.mainwindow, "Import exams", self.exam_dialog_path)
        if files:
            self.config.set_property(EXAM_DIALOG_PATH_KEY, os.path.dirname(files[0]))
        filtered = [x for x in files if x.lower().endswith(".jpg")]
        if len(filtered) > 0:
            self.exam_dialog_path = filtered[0]
        self.mainwindow.examcontroller.exams = filtered
        self.ui.statusbar.showMessage("Loaded {} exams".format(len(filtered)))

    def on_template_save(self):
        template_file = self.mainwindow.template_view_controller.selected_template
        if template_file is not None:
            if template_file.file is None:
                self.on_template_save_as()
                return

            if template_file.changed:
                self.save_file(template_file.file, template_file.template)
                template_file.changed = False
            else:
                self.ui.statusbar.showMessage("Template contains errors or no changes from last save.".format(template_file.file.name))

    def on_template_save_as(self):
        template_file = self.mainwindow.template_view_controller.selected_template
        if template_file is not None:
            fd = QFileDialog(self.mainwindow, "Save template", self.template_dialog_path)
            fd.setDefaultSuffix("template")
            fd.setAcceptMode(QFileDialog.AcceptSave)
            if fd.exec():
                filename = fd.selectedFiles()[0]
                file = open(filename, "w")
                template_file.file = file

                self.save_file(file, template_file.template)

                templates = self.mainwindow.template_list_controller.templates
                filename = template_file.file.name
                if filename not in templates:
                    templates.append(filename)
                    self.mainwindow.template_list_controller.templates = templates
                    index = self.ui.templateListView.selectionModel().model().createIndex(templates.index(filename), 0)
                    self.ui.templateListView.selectionModel().select(index, QItemSelectionModel.Select)

    def save_file(self, file, template):
        file.seek(0)
        file.write(template.to_json())
        file.truncate()
        self.ui.statusbar.showMessage("{} saved successfully.".format(file.name))

    def on_template_new(self):
        self.mainwindow.template_view_controller.selected_template = ""
