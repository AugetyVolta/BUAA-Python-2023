import random

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt, QDate, QObject, pyqtSignal, QThread
from PyQt5.QtGui import QIcon, QImage, QPixmap, QTransform
from qfluentwidgets import InfoBar, InfoBarPosition

from User.MyUserWidget_ui import Ui_MyUserWidget

humorous_sentences = [
    "吃什么？这问题比高考题还难，我都快需要用大数据分析来解决了！",
    "每次问我吃什么，我都开始怀疑人生，感觉选择餐厅比选择伴侣还要艰难啊！",
    "和我决定今晚吃什么，简直是斗智斗勇，我都怀疑自己是不是餐厅选择困难症患者了。",
    "吃饭这事，你得认真对待，毕竟这可能是影响你人生的一道重要选择啊！",
    "有的人信命，有的人信缘，而我只信菜单，因为上面写着我要吃的一切美味！",
    "我对吃的选择有个原则：今天吃什么，得保证我明天还想吃！",
    "人生苦短，我要吃我想吃的，这不叫贪嘴，叫对味道有追求！",
    "有人说吃是为了活着，我觉得我活着就是为了吃！",
    "关于吃什么，这得好好想一想"
]


class MyUserWidget(Ui_MyUserWidget, QWidget):
    def __init__(self, account):
        super().__init__()
        self.account = account  # 设置账户
        self.setupUi(self)
        # 设置头像
        self.setProfilePhoto()
        # 初始化用户信息
        self.initUserInfo()
        # 初始化signature
        self.signatureLable.setText(humorous_sentences[random.randint(0, len(humorous_sentences) - 1)])
        # 初始化性别选框
        self.initGenderComBox()
        # 初始化年龄选框
        self.initBirthdayComBox()
        # 设置修改个人信息按钮
        self.saveButton.clicked.connect(self.saveChangeInfo)

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

    def initGenderComBox(self):
        items = ['男', '女']
        self.genderComboBox.addItems(items)

    def initBirthdayComBox(self):
        items_year = [str(i) for i in range(1952, 2100)]
        items_month = [str(i) for i in range(1, 13)]
        items_day = [str(i) for i in range(1, 32)]
        self.birthday_year.addItems(items_year)
        self.birthday_month.addItems(items_month)
        self.birthday_day.addItems(items_day)

    def saveChangeInfo(self):
        new_nickname = self.nickNameEdit.text() if self.nickNameEdit.text() != '' else ""
        new_gender = self.genderComboBox.text() if self.genderComboBox.text() != '' else ""
        new_birth = self.birthday_year.text() + "-" + self.birthday_month.text() + '-' + self.birthday_day.text() if self.birthday_year.text() != '' else ""
        old_passwd = self.passwordEdit_old.text()
        new_passwd = self.passwordEdit_new.text()
        if old_passwd == '' and new_passwd == '':
            pass  # 不修改密码
        elif old_passwd != '' and new_passwd == '' or old_passwd == '' and new_passwd != '':
            self.createErrorInfoBar('请补全密码信息')
        else:
            pass
            # 首先验证原密码是否争取
            # 然后修改
        # TODO

    def createErrorInfoBar(self, content):
        InfoBar.error(
            title='错误',
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            # duration=-1,    # won't disappear automatically
            parent=self
        )
