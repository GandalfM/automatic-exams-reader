import sys
from PyQt5.QtWidgets import QApplication
from controllers.maincontroller import MainController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    aer = MainController()
    sys.exit(app.exec())