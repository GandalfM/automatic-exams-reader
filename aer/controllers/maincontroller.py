from PyQt5.QtWidgets import QMainWindow
from aer.config.configmanager import ConfigManager

from aer.controllers.examcontroller import ExamController
from aer.controllers.menucontroller import MenuController
from aer.controllers.templatelistcontroller import TemplateListController
from aer.controllers.templateviewcontroller import TemplateViewController
from aer.controllers.toolbarcontroller import ToolbarController
from aer.views.mainwindow import Ui_MainWindow


class MainController(QMainWindow):

    WINDOW_TITLE = "Automatic Exams Reader"

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.config_manager = ConfigManager()

        self.menucontroller = MenuController(self)
        self.toolbarcontroller = ToolbarController(self)

        self.template_view_controller = TemplateViewController(self)
        self.template_list_controller = TemplateListController(self)
        self.examcontroller = ExamController(self)

        self.show()
