# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'limits.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LimitsDialog(object):
    def setupUi(self, LimitsDialog):
        LimitsDialog.setObjectName("LimitsDialog")
        LimitsDialog.resize(398, 311)
        self.verticalLayoutWidget = QtWidgets.QWidget(LimitsDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 291))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.LimitsLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.LimitsLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.LimitsLayout.setContentsMargins(0, 0, 0, 0)
        self.LimitsLayout.setSpacing(5)
        self.LimitsLayout.setObjectName("LimitsLayout")
        self.limitsView = QtWidgets.QColumnView(self.verticalLayoutWidget)
        self.limitsView.setObjectName("limitsView")
        self.LimitsLayout.addWidget(self.limitsView)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.chooseTimeLimit = QtWidgets.QTimeEdit(self.verticalLayoutWidget)
        self.chooseTimeLimit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.chooseTimeLimit.setObjectName("chooseTimeLimit")
        self.horizontalLayout_2.addWidget(self.chooseTimeLimit)
        self.chooseAppLimitBox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.chooseAppLimitBox.setObjectName("chooseAppLimitBox")
        self.chooseAppLimitBox.addItem("")
        self.horizontalLayout_2.addWidget(self.chooseAppLimitBox)
        self.LimitsLayout.addLayout(self.horizontalLayout_2)
        self.addLimitButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.addLimitButton.setObjectName("addLimitButton")
        self.LimitsLayout.addWidget(self.addLimitButton)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.okLimitsButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.okLimitsButton.setObjectName("okLimitsButton")
        self.horizontalLayout.addWidget(self.okLimitsButton)
        self.LimitsLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(LimitsDialog)
        QtCore.QMetaObject.connectSlotsByName(LimitsDialog)

    def retranslateUi(self, LimitsDialog):
        _translate = QtCore.QCoreApplication.translate
        LimitsDialog.setWindowTitle(_translate("LimitsDialog", "Limits"))
        self.chooseAppLimitBox.setItemText(0, _translate("LimitsDialog", "all"))
        self.addLimitButton.setText(_translate("LimitsDialog", "Add Limit"))
        self.okLimitsButton.setText(_translate("LimitsDialog", "Ok"))
