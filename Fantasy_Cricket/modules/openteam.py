# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'openteam.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_openteamwindow(object):
    def setupUi(self, openteamwindow):
        openteamwindow.setObjectName("openteamwindow")
        openteamwindow.resize(300, 150)
        openteamwindow.setMinimumSize(QtCore.QSize(300, 130))
        openteamwindow.setMaximumSize(QtCore.QSize(300, 200))
        self.gridLayout = QtWidgets.QGridLayout(openteamwindow)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(openteamwindow)
        self.label.setStyleSheet("font: 75 14pt \"Comic Sans MS\";")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.comboBox = QtWidgets.QComboBox(openteamwindow)
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout.addWidget(self.comboBox)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.pushButton = QtWidgets.QPushButton(openteamwindow)
        self.pushButton.setStyleSheet("font: 10pt \"Segoe UI Historic\";")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 1, 0, 1, 1)

        self.retranslateUi(openteamwindow)
        QtCore.QMetaObject.connectSlotsByName(openteamwindow)

    def retranslateUi(self, openteamwindow):
        _translate = QtCore.QCoreApplication.translate
        openteamwindow.setWindowTitle(_translate("openteamwindow", "Open Team"))
        self.label.setText(_translate("openteamwindow", "Select your Team"))
        self.pushButton.setText(_translate("openteamwindow", "Open"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    openteamwindow = QtWidgets.QWidget()
    ui = Ui_openteamwindow()
    ui.setupUi(openteamwindow)
    openteamwindow.show()
    sys.exit(app.exec_())

