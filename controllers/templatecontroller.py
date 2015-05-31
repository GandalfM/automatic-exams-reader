from PyQt5.QtCore import QStringListModel


class TemplateController:

    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.ui = mainwindow.ui

        self._templates = []
        self._selectedtemplate = None

        self.ui.templateListView.clicked.connect(self.on_template_text_selection)

    def on_template_text_selection(self, index):
        self.selectedtemplate = self._templates[index.row()]

    @property
    def selectedtemplate(self):
        return self._selectedtemplate

    @selectedtemplate.setter
    def selectedtemplate(self, value):
        if self._selectedtemplate != value:
            self._selectedtemplate = value
            file = open(value.name, "r")
            content = file.read()
            self.ui.templateTextEdit.setText(content)

    @property
    def templates(self):
        return self._templates

    @templates.setter
    def templates(self, value):
        self._templates = value
        model = QStringListModel(map(lambda x: str(x), value))
        self.ui.templateListView.setModel(model)
