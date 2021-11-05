# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AppTime.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AppTime(object):
    def setupUi(self, AppTime):
        AppTime.setObjectName("AppTime")
        AppTime.setWindowModality(QtCore.Qt.NonModal)
        AppTime.setEnabled(True)
        AppTime.resize(666, 666)
        AppTime.setMinimumSize(QtCore.QSize(666, 666))
        AppTime.setMaximumSize(QtCore.QSize(666, 666))
        self.centralwidget = QtWidgets.QWidget(AppTime)
        self.centralwidget.setMinimumSize(QtCore.QSize(666, 666))
        self.centralwidget.setMaximumSize(QtCore.QSize(666, 666))
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 661, 651))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.mainLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 26)
        self.mainLayout.setObjectName("mainLayout")
        self.upLayout = QtWidgets.QHBoxLayout()
        self.upLayout.setObjectName("upLayout")
        self.userlayout = QtWidgets.QVBoxLayout()
        self.userlayout.setContentsMargins(6, -1, 6, -1)
        self.userlayout.setObjectName("userlayout")
        self.profilePhotoLayout = QtWidgets.QHBoxLayout()
        self.profilePhotoLayout.setObjectName("profilePhotoLayout")
        self.nameLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.nameLabel.setObjectName("nameLabel")
        self.profilePhotoLayout.addWidget(self.nameLabel)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.profilePhotoLayout.addItem(spacerItem)
        self.toolButton = QtWidgets.QToolButton(self.verticalLayoutWidget)
        self.toolButton.setObjectName("toolButton")
        self.profilePhotoLayout.addWidget(self.toolButton)
        self.userlayout.addLayout(self.profilePhotoLayout)
        self.downtimeLayout = QtWidgets.QHBoxLayout()
        self.downtimeLayout.setObjectName("downtimeLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.downtimeLayout.addItem(spacerItem1)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.downtimeLayout.addWidget(self.pushButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.downtimeLayout.addItem(spacerItem2)
        self.userlayout.addLayout(self.downtimeLayout)
        self.limitsLayout = QtWidgets.QHBoxLayout()
        self.limitsLayout.setObjectName("limitsLayout")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.limitsLayout.addItem(spacerItem3)
        self.limitsButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.limitsButton.setObjectName("limitsButton")
        self.limitsLayout.addWidget(self.limitsButton)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.limitsLayout.addItem(spacerItem4)
        self.userlayout.addLayout(self.limitsLayout)
        self.upLayout.addLayout(self.userlayout)
        self.day_layout = QtWidgets.QVBoxLayout()
        self.day_layout.setObjectName("day_layout")
        self.chooseDateLayout = QtWidgets.QHBoxLayout()
        self.chooseDateLayout.setObjectName("chooseDateLayout")
        self.featDate = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.featDate.setObjectName("featDate")
        self.chooseDateLayout.addWidget(self.featDate)
        self.weekdayBox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.weekdayBox.setObjectName("weekdayBox")
        self.weekdayBox.addItem("")
        self.weekdayBox.addItem("")
        self.chooseDateLayout.addWidget(self.weekdayBox)
        self.leftButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.leftButton.setObjectName("leftButton")
        self.chooseDateLayout.addWidget(self.leftButton)
        self.today = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.today.setObjectName("today")
        self.chooseDateLayout.addWidget(self.today)
        self.rightButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.rightButton.setObjectName("rightButton")
        self.chooseDateLayout.addWidget(self.rightButton)
        self.day_layout.addLayout(self.chooseDateLayout)
        self.statsLayout = QtWidgets.QVBoxLayout()
        self.statsLayout.setObjectName("statsLayout")
        self.generalStatsLayout = QtWidgets.QHBoxLayout()
        self.generalStatsLayout.setObjectName("generalStatsLayout")
        self.totalLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.totalLabel.setObjectName("totalLabel")
        self.generalStatsLayout.addWidget(self.totalLabel)
        self.differenceLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.differenceLabel.setObjectName("differenceLabel")
        self.generalStatsLayout.addWidget(self.differenceLabel)
        self.statsLayout.addLayout(self.generalStatsLayout)
        self.statsTable = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.statsTable.setObjectName("statsTable")
        self.statsTable.setColumnCount(0)
        self.statsTable.setRowCount(0)
        self.statsLayout.addWidget(self.statsTable)
        self.weekDays = QtWidgets.QHBoxLayout()
        self.weekDays.setObjectName("weekDays")
        self.mondayLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.mondayLabel.setObjectName("mondayLabel")
        self.weekDays.addWidget(self.mondayLabel)
        self.tuesdayLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.tuesdayLabel.setObjectName("tuesdayLabel")
        self.weekDays.addWidget(self.tuesdayLabel)
        self.wednesdayLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.wednesdayLabel.setObjectName("wednesdayLabel")
        self.weekDays.addWidget(self.wednesdayLabel)
        self.thursdayLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.thursdayLabel.setObjectName("thursdayLabel")
        self.weekDays.addWidget(self.thursdayLabel)
        self.fridayLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.fridayLabel.setObjectName("fridayLabel")
        self.weekDays.addWidget(self.fridayLabel)
        self.saturdayLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.saturdayLabel.setObjectName("saturdayLabel")
        self.weekDays.addWidget(self.saturdayLabel)
        self.sundayLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.sundayLabel.setObjectName("sundayLabel")
        self.weekDays.addWidget(self.sundayLabel)
        self.statsLayout.addLayout(self.weekDays)
        self.day_layout.addLayout(self.statsLayout)
        self.upLayout.addLayout(self.day_layout)
        self.mainLayout.addLayout(self.upLayout)
        self.showLayout = QtWidgets.QHBoxLayout()
        self.showLayout.setObjectName("showLayout")
        self.showLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.showLabel.setObjectName("showLabel")
        self.showLayout.addWidget(self.showLabel)
        self.appCatBox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.appCatBox.setObjectName("appCatBox")
        self.appCatBox.addItem("")
        self.appCatBox.addItem("")
        self.showLayout.addWidget(self.appCatBox)
        self.timeShowLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.timeShowLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.timeShowLabel.setObjectName("timeShowLabel")
        self.showLayout.addWidget(self.timeShowLabel)
        self.mainLayout.addLayout(self.showLayout)
        self.appsTimeTable = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.appsTimeTable.setEnabled(True)
        self.appsTimeTable.setMaximumSize(QtCore.QSize(666, 200))
        self.appsTimeTable.setObjectName("appsTimeTable")
        self.mainLayout.addWidget(self.appsTimeTable)
        AppTime.setCentralWidget(self.centralwidget)

        self.retranslateUi(AppTime)
        QtCore.QMetaObject.connectSlotsByName(AppTime)

    def retranslateUi(self, AppTime):
        _translate = QtCore.QCoreApplication.translate
        AppTime.setWindowTitle(_translate("AppTime", "AppTime"))
        self.nameLabel.setText(_translate("AppTime", "your name"))
        self.toolButton.setText(_translate("AppTime", "..."))
        self.pushButton.setText(_translate("AppTime", "Время отдыха"))
        self.limitsButton.setText(_translate("AppTime", "Лимиты"))
        self.featDate.setText(_translate("AppTime", "10 октября 2021"))
        self.weekdayBox.setItemText(0, _translate("AppTime", "day"))
        self.weekdayBox.setItemText(1, _translate("AppTime", "week"))
        self.leftButton.setText(_translate("AppTime", "<"))
        self.today.setText(_translate("AppTime", "Today"))
        self.rightButton.setText(_translate("AppTime", ">"))
        self.totalLabel.setText(_translate("AppTime", "Обшее время: "))
        self.differenceLabel.setText(_translate("AppTime", "Разница с прошлым днем: "))
        self.mondayLabel.setText(_translate("AppTime", "пон"))
        self.tuesdayLabel.setText(_translate("AppTime", "втр"))
        self.wednesdayLabel.setText(_translate("AppTime", "сре"))
        self.thursdayLabel.setText(_translate("AppTime", "чет"))
        self.fridayLabel.setText(_translate("AppTime", "пят"))
        self.saturdayLabel.setText(_translate("AppTime", "суб"))
        self.sundayLabel.setText(_translate("AppTime", "вос"))
        self.showLabel.setText(_translate("AppTime", "Показать:"))
        self.appCatBox.setItemText(0, _translate("AppTime", "Приложения"))
        self.appCatBox.setItemText(1, _translate("AppTime", "Категории"))
        self.timeShowLabel.setText(_translate("AppTime", "Время:"))
