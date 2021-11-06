import sys

from PyQt5.QtCore import QTime, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QErrorMessage, QMessageBox

from AppTimeUI import Ui_AppTime
from LimitsUI import Ui_LimitsDialog
from DowntimeUI import Ui_downTimeDialog

import datetime


class DownTimeDialog(QDialog, Ui_downTimeDialog):
    def __init__(self, parent=None):
        self._parent = parent
        super(DownTimeDialog, self).__init__(parent)
        self.setupUi(self)
        self.resetTimeButton.clicked.connect(self.reset_time)
        self.applyTimeButton.clicked.connect(self.apply_time)

    def reset_time(self):
        self.startTimeEdit.setTime(QTime(0, 0))
        self.endTimeEdit.setTime(QTime(0, 0))

    def apply_time(self):
        start_hours, start_minutes = self.startTimeEdit.time().hour(), self.startTimeEdit.time().minute()
        end_hours, end_minutes = self.endTimeEdit.time().hour(), self.endTimeEdit.time().minute()
        # if start_hours > end_hours or (start_hours == end_hours and start_minutes > end_minutes):
        # else:
        # save to db
        self.close()

    def closeEvent(self, a0):
        self._parent.setEnabled(True)


class LimitsDialog(QDialog, Ui_LimitsDialog):
    def __init__(self, parent=None):
        self._parent = parent
        super().__init__(parent)
        self.setupUi(self)
        # get limits from db

        self.okLimitsButton.clicked.connect(self.ok_pressed)

    def ok_pressed(self):
        self.close()

    def closeEvent(self, a0):
        self._parent.setEnabled(True)


class MainWindow(QMainWindow, Ui_AppTime):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.chosenDate = datetime.date.today()
        self.featDate.setText(self.chosenDate.strftime('%d %B %Y'))
        self.limitsButton.clicked.connect(self.show_limits_dialog)
        self.downtimeButton.clicked.connect(self.show_downtime_dialog)
        self.updateButton.clicked.connect(
            lambda: QMessageBox.about(self, "Update", "It's up to date") and self.update_())
        self.todayButton.clicked.connect(self.today_button_clicked)
        self.leftButton.clicked.connect(self.left_button_clicked)
        self.rightButton.clicked.connect(self.right_button_clicked)

    def left_button_clicked(self):
        if self.weekdayBox.currentText() == 'day':
            self.chosenDate -= datetime.timedelta(days=1)
            self.update_()
        else:
            self.chosenDate -= datetime.timedelta(days=7)
            self.update_()

    def right_button_clicked(self):
        if self.weekdayBox.currentData() == 'day':
            if self.chosenDate != datetime.date.today():
                self.chosenDate += datetime.timedelta(days=1)
                self.update_()
        else:
            self.chosenDate = min(datetime.timedelta(days=7) + self.chosenDate, datetime.date.today())
            self.update_()

    def today_button_clicked(self):
        self.chosenDate = datetime.date.today()
        self.update_()

    def update_(self):
        self.featDate.setText(self.chosenDate.strftime('%d %B %Y'))
        # QMessageBox.about(self, "Update", "It's up to date")
        pass  # update frames

    def show_limits_dialog(self):
        self.setEnabled(False)
        dialog_window = LimitsDialog(self)
        dialog_window.exec_()

    def show_downtime_dialog(self):
        self.setEnabled(False)
        dialog_window = DownTimeDialog(self)
        dialog_window.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./appIcon.jpg"))
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
