from PyQt5.QtWidgets import QMainWindow

from aer.controllers.examcontroller import ExamController
from aer.controllers.menucontroller import MenuController
from aer.controllers.templatelistcontroller import TemplateListController
from aer.controllers.templateviewcontroller import TemplateViewController
from aer.views.mainwindow import Ui_MainWindow


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
