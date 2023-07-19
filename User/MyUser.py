from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QMessageBox
from PyQt5.QtCore import Qt, QDate, QObject, pyqtSignal, QThread
from PyQt5.QtGui import QIcon, QImage, QPixmap, QTransform

from User.MyUserWidget_ui import Ui_MyUserWidget


class MyUserWidget(Ui_MyUserWidget, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
