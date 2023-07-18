# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'findAndReplace.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDesktopWidget


class Ui_FindAndReplaceDlg(object):
    def setupUi(self, FindAndReplaceDlg):
        FindAndReplaceDlg.setObjectName("FindAndReplaceDlg")
        FindAndReplaceDlg.resize(424, 180)
        self.line = QtWidgets.QFrame(FindAndReplaceDlg)
        self.line.setGeometry(QtCore.QRect(297, 9, 20, 161))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.widget = QtWidgets.QWidget(FindAndReplaceDlg)
        self.widget.setGeometry(QtCore.QRect(10, 9, 286, 158))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.findLineEdit = QtWidgets.QLineEdit(self.widget)
        self.findLineEdit.setObjectName("findLineEdit")
        self.gridLayout.addWidget(self.findLineEdit, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.replaceLineEdit = QtWidgets.QLineEdit(self.widget)
        self.replaceLineEdit.setObjectName("replaceLineEdit")
        self.gridLayout.addWidget(self.replaceLineEdit, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.caseCheckBox = QtWidgets.QCheckBox(self.widget)
        self.caseCheckBox.setObjectName("caseCheckBox")
        self.horizontalLayout.addWidget(self.caseCheckBox)
        self.wholeCheckBox = QtWidgets.QCheckBox(self.widget)
        self.wholeCheckBox.setChecked(False)
        self.wholeCheckBox.setObjectName("wholeCheckBox")
        self.horizontalLayout.addWidget(self.wholeCheckBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.syntaxComboBox = QtWidgets.QComboBox(self.widget)
        self.syntaxComboBox.setObjectName("syntaxComboBox")
        self.syntaxComboBox.addItem("")
        self.syntaxComboBox.addItem("")
        self.horizontalLayout_2.addWidget(self.syntaxComboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.widget1 = QtWidgets.QWidget(FindAndReplaceDlg)
        self.widget1.setGeometry(QtCore.QRect(316, 10, 99, 155))
        self.widget1.setObjectName("widget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.findButton = QtWidgets.QPushButton(self.widget1)
        self.findButton.setObjectName("findButton")
        self.verticalLayout_2.addWidget(self.findButton)
        self.replaceButton = QtWidgets.QPushButton(self.widget1)
        self.replaceButton.setObjectName("replaceButton")
        self.verticalLayout_2.addWidget(self.replaceButton)
        self.replaceAllButton = QtWidgets.QPushButton(self.widget1)
        self.replaceAllButton.setObjectName("replaceAllButton")
        self.verticalLayout_2.addWidget(self.replaceAllButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem1)
        self.closeButton = QtWidgets.QPushButton(self.widget1)
        self.closeButton.setObjectName("closeButton")
        self.verticalLayout_2.addWidget(self.closeButton)
        self.label.setBuddy(self.findLineEdit)
        self.label_2.setBuddy(self.replaceLineEdit)
        self.label_3.setBuddy(self.syntaxComboBox)

        self.retranslateUi(FindAndReplaceDlg)
        self.closeButton.clicked.connect(FindAndReplaceDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(FindAndReplaceDlg)

    def retranslateUi(self, FindAndReplaceDlg):
        _translate = QtCore.QCoreApplication.translate
        FindAndReplaceDlg.setWindowTitle(_translate("FindAndReplaceDlg", "Find and Replace"))
        self.label.setText(_translate("FindAndReplaceDlg", "Find &what:"))
        self.label_2.setText(_translate("FindAndReplaceDlg", "Replace with:"))
        self.caseCheckBox.setText(_translate("FindAndReplaceDlg", "&Case sensitive"))
        self.wholeCheckBox.setText(_translate("FindAndReplaceDlg", "Wh&ole words"))
        self.label_3.setText(_translate("FindAndReplaceDlg", "&Syntax:"))
        self.syntaxComboBox.setItemText(0, _translate("FindAndReplaceDlg", "Literal text"))
        self.syntaxComboBox.setItemText(1, _translate("FindAndReplaceDlg", "Regular expression"))
        self.findButton.setText(_translate("FindAndReplaceDlg", "&Find"))
        self.replaceButton.setText(_translate("FindAndReplaceDlg", "&Replace"))
        self.replaceAllButton.setText(_translate("FindAndReplaceDlg", "Replace &All"))
        self.closeButton.setText(_translate("FindAndReplaceDlg", "Close"))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

