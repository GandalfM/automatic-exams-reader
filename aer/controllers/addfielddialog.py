from PyQt5.QtWidgets import QDialog
from aer.views.addfielddialog import Ui_AddFieldDialog
from enum import Enum


class FieldType(Enum):
    MARK = 1
    HANDWRITTEN = 2
    PRINTED = 3


class AddFieldDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.ui = Ui_AddFieldDialog()
        self.ui.setupUi(self)

        self.ui.buttonBox.accepted.connect(self._accepted)
        self.ui.buttonBox.rejected.connect(self._rejected)

    @property
    def name(self):
        return self.ui.name.text()

    @name.setter
    def name(self, value):
        self.ui.name.setText(value)

    @property
    def field_type(self):
        if self.ui.radioHandwritten.isChecked():
            return FieldType.HANDWRITTEN
        if self.ui.radioMarked.isChecked():
            return FieldType.MARK
        if self.ui.radioPrinted.isChecked():
            return FieldType.PRINTED

    def _validate(self):
        return not self.name.isspace()

    def _accepted(self):
        self.ok = self._validate()
        self.close()

    def _rejected(self):
        self.ok = False
        self.close()

    def show(self, name=""):
        self.name = name
        self.exec_()
