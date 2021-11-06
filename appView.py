import sqlite3
import sys

from PyQt5.QtCore import QTime, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QErrorMessage, QMessageBox, QHBoxLayout, QLabel, \
    QTreeWidgetItem

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
        self.connection = sqlite3.connect("./AppTime_db.sqlite")
        self.chosenDate = datetime.date.today()
        self.featDate.setText(self.chosenDate.strftime('%d %B %Y'))
        self.limitsButton.clicked.connect(self.show_limits_dialog)
        self.downtimeButton.clicked.connect(self.show_downtime_dialog)
        self.updateButton.clicked.connect(
            lambda: self.update_window() or QMessageBox.about(self, "Update", "It's up to date"))
        self.todayButton.clicked.connect(self.today_button_clicked)
        self.leftButton.clicked.connect(self.left_button_clicked)
        self.rightButton.clicked.connect(self.right_button_clicked)
        self.update_window()

    def left_button_clicked(self):
        if self.weekdayBox.currentText() == 'day':
            self.chosenDate -= datetime.timedelta(days=1)
            self.update_window()
        else:
            self.chosenDate -= datetime.timedelta(days=7)
            self.update_window()

    def right_button_clicked(self):
        if self.weekdayBox.currentText() == 'day':
            if self.chosenDate != datetime.date.today():
                self.chosenDate += datetime.timedelta(days=1)
                self.update_window()
        else:
            self.chosenDate = min(datetime.timedelta(days=7) + self.chosenDate, datetime.date.today())
            self.update_window()

    def today_button_clicked(self):
        self.chosenDate = datetime.date.today()
        self.update_window()

    def show_data(self, apps_usage, total_week):
        for_day = sum(apps_usage.values())
        hours = int(for_day // 3600)
        minutes = int(for_day // 60 - hours * 60)
        # show data on labels
        if hours:
            self.totalLabel.setText(f"Всего: {hours} ч. {minutes} мин.")
        elif minutes:
            self.totalLabel.setText(f"Всего: {minutes} мин.")
        else:
            self.totalLabel.setText(f"Всего: {int(for_day - hours * 3600 - minutes * 60)} сек.")
        # set up lowest table
        self.appsTimeTable.clear()
        for item in reversed(sorted(apps_usage.items(), key=lambda x: (x[1], x[0]))):
            app_name, total_time = item[0], item[1]
            hours = int(total_time // 3600)
            minutes = int(total_time // 60 - hours * 60)
            if hours:
                total_time = f"{hours} ч. {minutes} мин."
            elif minutes:
                total_time = f"{minutes} мин."
            else:
                total_time = f"{int(total_time - hours * 3600 - minutes * 60)} сек."
            print(app_name, total_time)
            element = QTreeWidgetItem(self.appsTimeTable)
            element.setText(0, app_name)
            element.setText(1, total_time)
            self.appsTimeTable.addTopLevelItem(element)

    def update_window(self):
        self.featDate.setText(self.chosenDate.strftime('%d %B %Y'))
        # QMessageBox.about(self, "Update", "It's up to date")
        total_week, apps_usage = self.get_week_info(self.chosenDate)
        if self.weekdayBox.currentText() == 'day':
            apps_usage = self.get_day_info(self.chosenDate)
        self.show_data(apps_usage, total_week)

    def show_limits_dialog(self):
        self.setEnabled(False)
        dialog_window = LimitsDialog(self)
        dialog_window.exec_()

    def show_downtime_dialog(self):
        self.setEnabled(False)
        dialog_window = DownTimeDialog(self)
        dialog_window.exec_()

    def get_day_info(self, day):
        day_id = self.connection.cursor().execute(
            f"""SELECT id FROM days WHERE day_name='{day.strftime("%Y-%m-%d")}'""").fetchone()
        if not day_id:
            return {}
        day_id = day_id[0]
        app_time_ids = self.connection.cursor().execute(
            f"""SELECT app_time_id FROM apps_time WHERE day_id={day_id}""").fetchall()
        day_apps_usage = {}
        for app_time_id in app_time_ids:
            this_day_app_usage = self.connection.cursor().execute(
                f"""SELECT app_name, time FROM app_time WHERE id={app_time_id[0]}""").fetchone()
            if this_day_app_usage:
                day_apps_usage[this_day_app_usage[0]] = this_day_app_usage[1]
        return day_apps_usage

    def get_week_info(self, day):
        monday = day - datetime.timedelta(days=day.weekday())
        total_week = []
        apps_usage = {}
        for delta in range(7):
            total_week.append(0)
            current_data = monday + datetime.timedelta(days=delta)
            day_id = self.connection.cursor().execute(
                f"""SELECT id FROM days WHERE day_name='{current_data.strftime("%Y-%m-%d")}'""").fetchone()
            if not day_id:
                continue
            day_id = day_id[0]
            app_time_ids = self.connection.cursor().execute(
                f"""SELECT app_time_id FROM apps_time WHERE day_id={day_id}""").fetchall()
            for app_time_id in app_time_ids:
                this_day_app_usage = self.connection.cursor().execute(
                    f"""SELECT app_name, time FROM app_time WHERE id={app_time_id[0]}""").fetchone()
                if this_day_app_usage:
                    apps_usage[this_day_app_usage[0]] = \
                        this_day_app_usage[1] if this_day_app_usage[0] not in apps_usage \
                            else this_day_app_usage[this_day_app_usage[0]] + this_day_app_usage[1]
                    total_week[-1] += this_day_app_usage[1]
        return total_week, apps_usage

    def closeEvent(self, a0) -> None:
        self.connection.close()


def process_week_data(total_week):
    upper_bound = max(total_week) * 1.25
    coefficient = upper_bound / 250
    total_week = list(map(lambda x: int(x * coefficient), total_week))
    return total_week


def get_week_plot(total_week):
    total_week = process_week_data(total_week)
    x = [coord for coord in range(12, 502)]
    y = []
    for day in range(7):
        y.extend([0 for _ in range(10)])
        y.extend([total_week[day] for _ in range(50)])
        y.extend([0 for _ in range(10)])
    return x, y


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./appIcon.jpg"))
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
