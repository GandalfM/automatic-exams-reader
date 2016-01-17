import os

from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QMessageBox

from aer.config.configconstants import *


class TemplateListController:

    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.config = self.mainwindow.config_manager
        self.ui = mainwindow.ui
        self._template_view_controller = mainwindow.template_view_controller

        templates = self.config.get_property(TEMPLATES_LOADED, [])
        for temp in templates:
            if not os.path.exists(temp):
                templates.remove(temp)

        self.templates = templates
        self._selected_template = None
        self.ui.templateListView.clicked.connect(self.on_template_text_selection)

    def on_template_text_selection(self, index):
        self.selected_template = self._templates[index.row()]

    @property
    def selected_template(self):
        return self._selected_template

    @selected_template.setter
    def selected_template(self, value):
        if self._selected_template != value:
            if os.path.exists(value):
                self._template_view_controller.selected_template = value
                self._selected_template = value
            else:
                QMessageBox.warning(self.mainwindow, "Warning", "No template file under this path")

    @property
    def templates(self):
        return self._templates

    @templates.setter
    def templates(self, value):
        self._templates = value
        model = QStringListModel(map(lambda x: str(x), value))
        self.ui.templateListView.setModel(model)
