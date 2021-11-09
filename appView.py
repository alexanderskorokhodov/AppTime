import sqlite3
import sys

from PyQt5.QtCore import QTime
from PyQt5.QtGui import QIcon, QPainter, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QTreeWidgetItem, QTreeWidget

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
    def __init__(self, parent=None, connection=None):
        self._parent = parent
        self.connection = connection
        self.apps = self.connection.cursor().execute(f"""SELECT DISTINCT app_name FROM app_time""").fetchall()
        self.connection.commit()
        self.apps = list(map(lambda x: x[0], self.apps))
        self.limits = self.connection.cursor().execute(f"""SELECT id, app_name, time FROM limits""").fetchall()
        super().__init__(parent)
        self.setupUi(self)
        for i, app_name in enumerate(self.apps):
            self.chooseAppLimitBox.addItem(app_name, i)
        self.show_limits()
        self.okLimitsButton.clicked.connect(self.ok_pressed)
        self.removeLimitButton.clicked.connect(self.delete_limit)
        self.addLimitButton.clicked.connect(self.add_limit)

    def add_limit(self):
        app_name = self.chooseAppLimitBox.currentText()
        app_time = list(map(int, self.chooseTimeLimit.text().split(':')))
        app_time = app_time[0] * 3600 + app_time[1] * 60
        if app_name == 'all':
            app_name = '\\' + app_name
        if app_name not in list(map(lambda x: x[1], self.limits)):
            if app_time > 0:
                self.limits.append((len(self.limits), app_name, app_time))
                self.show_limits()
            else:
                QMessageBox.about(self, "Error", "Time limit can't be zero!")
        else:
            QMessageBox.about(self, "Error", "You have this app limit!")

    def delete_limit(self):
        if self.limits:
            ind = self.limitsView.currentIndex().row()
            item = QTreeWidget.invisibleRootItem(self.limitsView).takeChild(ind)
            app_time = item.text(1)
            if app_time.endswith(' ч.'):
                app_time = float(app_time[:-3]) * 3600
            elif ' ч.' in app_time:
                app_time = app_time[:-5].split('ч. ')
                app_time = float(app_time[0]) * 3600 + float(app_time[1]) * 60
            else:
                app_time = float(app_time[:-5]) * 60
            item = (item.text(0), app_time)
            for i in self.limits:
                if i[1:] == item:
                    self.limits.remove(i)

    def show_limits(self):
        self.limitsView.clear()
        for limit in self.limits[::-1]:
            app_name = limit[1]
            hours, minutes = int(limit[2] // 3600), int(limit[2] % 3600) // 60
            if hours and minutes:
                app_time = f"{hours} ч. {minutes} мин."
            elif hours:
                app_time = f"{hours} ч."
            else:
                app_time = f'{minutes} мин.'
            element = QTreeWidgetItem(self.limitsView)
            element.setText(0, app_name)
            element.setText(1, app_time)
            self.limitsView.addTopLevelItem(element)

    def ok_pressed(self):
        self.connection.cursor().execute("""DELETE FROM limits""")
        self.connection.commit()
        if self.limits:
            self.connection.cursor().executemany("""INSERT INTO limits (id, app_name, time) VALUES (?, ?, ?);""",
                                                 self.limits)
            self.connection.commit()
        with open(file="UpdateLimits.txt", mode='w') as updateFile:
            updateFile.write('1')
        self.close()

    def closeEvent(self, a0):
        self._parent.setEnabled(True)


class MainWindow(QMainWindow, Ui_AppTime):
    def __init__(self):
        super().__init__()
        self.total_week = []
        self.setupUi(self)
        self.week_days = [self.mondayLabel, self.tuesdayLabel, self.wednesdayLabel, self.thursdayLabel,
                          self.fridayLabel, self.saturdayLabel, self.sundayLabel]
        self.connection = sqlite3.connect("./AppTime_db.sqlite")
        self.chosenDate = datetime.date.today()
        self.featDate.setText(self.chosenDate.strftime('%d %B %Y'))
        self.limitsButton.clicked.connect(self.show_limits_dialog)
        self.downtimeButton.clicked.connect(self.show_downtime_dialog)
        self.updateButton.clicked.connect(self.update_window)
        self.todayButton.clicked.connect(self.today_button_clicked)
        self.leftButton.clicked.connect(self.left_button_clicked)
        self.rightButton.clicked.connect(self.right_button_clicked)
        self.downtimeButton.hide()
        self.update_window()

    # def keyPressEvent(self, a0):
    #     if a0.key() == Qt.Key_Left:
    #         self.left_button_clicked()
    #     elif a0.key() == Qt.Key_Right:
    #         self.right_button_clicked()

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

    def paintEvent(self, a0):
        qp = QPainter()
        qp.begin(self)
        # qp.setBrush(QColor(255, 255, 255))
        if self.total_week:
            for day in range(7):
                if day == self.chosenDate.weekday():
                    qp.setBrush(QColor(26, 36, 117))
                else:
                    qp.setBrush(QColor(162, 167, 207))
                qp.drawRect(230 + day * 70, 330, 60, -self.total_week[day])
        qp.end()

    def show_data(self, apps_usage, total_week):
        try:
            for_day = apps_usage['\\all']
        except:
            for_day = 0
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
            if app_name == '\\all':
                continue
            hours = int(total_time // 3600)
            minutes = int(total_time // 60 - hours * 60)
            if hours:
                total_time = f"{hours} ч. {minutes} мин."
            elif minutes:
                total_time = f"{minutes} мин."
            else:
                total_time = f"{int(total_time - hours * 3600 - minutes * 60)} сек."
            element = QTreeWidgetItem(self.appsTimeTable)
            element.setText(0, app_name)
            element.setText(1, total_time)
            self.appsTimeTable.addTopLevelItem(element)
        self.total_week = process_week_data(total_week)
        self.repaint()

    def update_window(self):
        for day in self.week_days:
            day.setEnabled(True)
        self.featDate.setText(self.chosenDate.strftime('%d %B %Y'))
        # QMessageBox.about(self, "Update", "It's up to date")
        total_week, apps_usage = self.get_week_info(self.chosenDate)
        if self.weekdayBox.currentText() == 'day':
            apps_usage = self.get_day_info(self.chosenDate)
            try:
                prev = self.get_day_info(self.chosenDate - datetime.timedelta(days=1))
                if prev:
                    percs = int(apps_usage["\\all"] / prev["\\all"] * 100 - 100)
                    self.differenceLabel.setText(f"Разница с прошлым днем {percs}%")
            except:
                self.differenceLabel.setText(f"Разница с прошлым днем -%")
        else:
            try:
                _, prev = self.get_week_info(self.chosenDate - datetime.timedelta(days=7))
                if prev:
                    percs = int(apps_usage["\\all"] / prev["\\all"] * 100 - 100)
                    self.differenceLabel.setText(f"Разница с прошлой неделей {percs}%")
            except:
                self.differenceLabel.setText(f"Разница с прошлой неделей -%")
        self.show_data(apps_usage, total_week)
        for day in self.week_days[:self.chosenDate.weekday()] + self.week_days[self.chosenDate.weekday() + 1:]:
            day.setEnabled(False)

    def show_limits_dialog(self):
        self.setEnabled(False)
        dialog_window = LimitsDialog(self, self.connection)
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
                if this_day_app_usage[0] == "\\all":
                    total_week[-1] = this_day_app_usage[1]
                    continue
                if this_day_app_usage:
                    apps_usage[this_day_app_usage[0]] = \
                        this_day_app_usage[1] if this_day_app_usage[0] not in apps_usage \
                            else apps_usage[this_day_app_usage[0]] + this_day_app_usage[1]

        return total_week, apps_usage

    def closeEvent(self, a0) -> None:
        self.connection.close()


def process_week_data(total_week):
    upper_bound = max(total_week) * 1.25
    if upper_bound == 0:
        return total_week
    coefficient = upper_bound / 250
    total_week = list(map(lambda x: int(x / coefficient), total_week))
    return total_week


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./appIcon.jpg"))
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
