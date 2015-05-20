from PyQt5.QtWidgets import QMainWindow
from views.mainwindow import Ui_MainWindow


class MainController(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()