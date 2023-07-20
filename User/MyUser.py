from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt, QDate, QObject, pyqtSignal, QThread
from PyQt5.QtGui import QIcon, QImage, QPixmap, QTransform

from User.MyUserWidget_ui import Ui_MyUserWidget


class MyUserWidget(Ui_MyUserWidget, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 设置头像
        self.setProfilePhoto()
        # 初始化用户信息
        self.initUserInfo()

        self.ProgressRing.setValue(50)
        self.ProgressRing.setTextVisible(True)

        print(self.stackedWidget.count())

    # 初始化个人信息
    def initUserInfo(self):
        # 设置第一页为首页
        self.stackedWidget.setCurrentIndex(0)
        self.SegmentedWidget.addItem('userInfo', '个人信息', self.setFirstPage, )
        self.SegmentedWidget.addItem('edit', '编辑', self.setSecondPage, )
        self.SegmentedWidget.setCurrentItem('userInfo')

    def setFirstPage(self):
        self.stackedWidget.setCurrentIndex(0)

    def setSecondPage(self):
        self.stackedWidget.setCurrentIndex(1)

    # 设置头像
    def setProfilePhoto(self):
        pixmap = QPixmap("{}/../picture_set/BUAA_128x128.jpg")
        self.ImageLabel.setPixmap(pixmap)
        self.ImageLabel.setScaledContents(True)
        self.ImageLabel.clicked.connect(self.uploadProfilePhoto)

    # 更新头像
    def uploadProfilePhoto(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter('Images (*.png *.xpm *.jpg *.bmp)')
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            # 在这里执行上传头像的逻辑，这里只是简单地显示选择的图像
            pixmap = QPixmap(file_path)
            self.ImageLabel.setPixmap(pixmap.scaled(self.ImageLabel.width(), self.ImageLabel.height()))
