# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MyFavoriteWidget_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MyFavoriteWidget(object):
    def setupUi(self, MyFavoriteWidget):
        MyFavoriteWidget.setObjectName("MyFavoriteWidget")
        MyFavoriteWidget.resize(1032, 663)
        self.layoutWidget = QtWidgets.QWidget(MyFavoriteWidget)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 50, 979, 58))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(838, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.TitleLabel = TitleLabel(self.layoutWidget)
        self.TitleLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.TitleLabel.setProperty("pixelFontSize", 32)
        self.TitleLabel.setObjectName("TitleLabel")
        self.horizontalLayout.addWidget(self.TitleLabel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(self.layoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.CardWidget = CardWidget(MyFavoriteWidget)
        self.CardWidget.setGeometry(QtCore.QRect(20, 120, 481, 521))
        self.CardWidget.setObjectName("CardWidget")
        self.CardWidget_3 = CardWidget(MyFavoriteWidget)
        self.CardWidget_3.setGeometry(QtCore.QRect(520, 120, 481, 521))
        self.CardWidget_3.setObjectName("CardWidget_3")

        self.retranslateUi(MyFavoriteWidget)
        QtCore.QMetaObject.connectSlotsByName(MyFavoriteWidget)

    def retranslateUi(self, MyFavoriteWidget):
        _translate = QtCore.QCoreApplication.translate
        MyFavoriteWidget.setWindowTitle(_translate("MyFavoriteWidget", "Form"))
        self.TitleLabel.setText(_translate("MyFavoriteWidget", "我的收藏"))
from qfluentwidgets import CardWidget, TitleLabel
