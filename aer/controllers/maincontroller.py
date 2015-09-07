from PyQt5.QtWidgets import QMainWindow

from controllers.examcontroller import ExamController
from controllers.menucontroller import MenuController
from controllers.templatelistcontroller import TemplateListController
from aer.controllers.templateviewcontroller import TemplateViewController
from views.mainwindow import Ui_MainWindow


class MainController(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.menucontroller = MenuController(self)

        self.template_view_controller = TemplateViewController(self)
        self.template_list_controller = TemplateListController(self)
        self.examcontroller = ExamController(self)

        self.show()
