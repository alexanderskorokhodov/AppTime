import sys
import sqlite3
from AppTimeUI import Ui_AppTime
from LimitsUI import Ui_LimitsDialog
from PyQt5.QtWidgets import QApplication, QMainWindow


class LimitsDialog(QMainWindow, Ui_LimitsDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class MainWindow(QMainWindow, Ui_AppTime):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.limitsButton.clicked.connect(self.showLimitsDialog)

    def showLimitsDialog(self):
        dialog_window = LimitsDialog()
        dialog_window.show()
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
