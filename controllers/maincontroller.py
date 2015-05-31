from PyQt5.QtWidgets import QMainWindow

from controllers.menucontroller import MenuController
from controllers.templatecontroller import TemplateController
from views.mainwindow import Ui_MainWindow


class MainController(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.menucontroller = MenuController(self)
        self.templatecontroller = TemplateController(self)

        self.show()
