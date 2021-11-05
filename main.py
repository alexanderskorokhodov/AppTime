import sys
import sqlite3
from AppTimeUI import Ui_AppTime
from LimitsUI import Ui_LimitsDialog
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog


class LimitsDialog(QDialog, Ui_LimitsDialog):
    def __init__(self, parent=None):
        self._parent = parent
        super().__init__(parent)
        self.setupUi(self)
        self.okLimitsButton.clicked.connect(self.ok_pressed)

    def ok_pressed(self):
        self.close()

    def closeEvent(self, a):
        self._parent.show()


class MainWindow(QMainWindow, Ui_AppTime):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.limitsButton.clicked.connect(self.show_limits_dialog)

    def show_limits_dialog(self):
        self.hide()
        dialog_window = LimitsDialog(self)
        dialog_window.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
