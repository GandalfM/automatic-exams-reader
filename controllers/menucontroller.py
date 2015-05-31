from PyQt5.QtWidgets import QFileDialog

from domain.template import Template


class MenuController:

    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.ui = mainwindow.ui

        self.ui.actionTemplateOpen.triggered.connect(self.on_template_open_triggered)

    def on_template_open_triggered(self):
        files = QFileDialog.getOpenFileNames(self.mainwindow, "Open template")
        filtered = [Template(x) for x in files[0] if x.endswith(".py")]
        self.mainwindow.templatecontroller.templates = filtered
        self.ui.statusbar.showMessage("Loaded {} templates".format(len(filtered)))