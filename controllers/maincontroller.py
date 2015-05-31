from PyQt5.QtCore import QStringListModel

from PyQt5.QtWidgets import QMainWindow

from controllers.menucontroller import MenuController
from views.mainwindow import Ui_MainWindow


class MainController(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.menucontroller = MenuController(self)

        self._templates = []

        self.show()

    @property
    def templates(self):
        return self._templates

    @templates.setter
    def templates(self, value):
        self._templates = value
        model = QStringListModel(map(lambda x: str(x), value))
        self.ui.templateListView.setModel(model)
