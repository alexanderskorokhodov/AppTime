import sys

from PyQt5.QtCore import QTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog

from AppTimeUI import Ui_AppTime
from LimitsUI import Ui_LimitsDialog
from DowntimeUI import Ui_downTimeDialog


class DownTimeDialog(QDialog, Ui_downTimeDialog):
    def __init__(self, parent=None):
        self._parent = parent
        super(DownTimeDialog, self).__init__(parent)
        self.setupUi(self)

    def reset_downtime(self):
        self.startTimeEdit.setTime(QTime(0, 0))
        self.endTimeEdit.setTime(QTime(0, 0))

    def apply_time(self):
        start_hours, start_minutes = self.startTimeEdit.time().hour(), self.startTimeEdit.time().minute()
        end_hours, end_minutes = self.startTimeEdit.time().hour(), self.startTimeEdit.time().minute()
        print(start_hours, start_minutes, end_hours, end_minutes)
        if start_hours > end_hours or (start_hours == end_hours and start_minutes> end_minutes):
            print('check')
        else:
            # save to db
            self.close()

    def closeEvent(self, a0):
        self._parent.show()


class LimitsDialog(QDialog, Ui_LimitsDialog):
    def __init__(self, parent=None):
        self._parent = parent
        super().__init__(parent)
        self.setupUi(self)
        self.okLimitsButton.clicked.connect(self.ok_pressed)

    def ok_pressed(self):
        self.close()

    def closeEvent(self, a0):
        self._parent.show()


class MainWindow(QMainWindow, Ui_AppTime):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.limitsButton.clicked.connect(self.show_limits_dialog)
        self.downtimeButton.clicked.connect(self.show_downtime_dialog)

    def show_limits_dialog(self):
        self.hide()
        dialog_window = LimitsDialog(self)
        dialog_window.exec_()

    def show_downtime_dialog(self):
        self.hide()
        dialog_window = DownTimeDialog(self)
        dialog_window.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./appIcon.jpg"))
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
