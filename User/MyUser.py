import random
import sys

from PIL.Image import Image
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QMessageBox, QFileDialog, QApplication
from PyQt5.QtCore import Qt, QDate, QObject, pyqtSignal, QThread
from PyQt5.QtGui import QIcon, QImage, QPixmap, QTransform
from qfluentwidgets import InfoBar, InfoBarPosition

from DataBase.database import DBOperator
from picture_set import pic_rc
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
        self.initUserEdit()
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
        # 设置个人信息,头像,昵称，用户名，性别，生日，收藏数，吃过数
        # (name,nick, passwd,sex,birth,fav,ates,photo)
        database = DBOperator()
        person = database.get_person(self.account)
        name = person[0]
        nick = person[1]
        if person[3] == 0:
            sex = 'Not edited yet'
        elif person[3] == 1:
            sex = '男'
        else:
            sex = '女'
        birth = person[4] if person[4] != '' else 'Not edited yet'
        fav = person[5]
        ates = person[6]
        self.userNameShow.setText(name)
        self.nickNameShow.setText(nick)
        self.UserName.setText(nick)
        self.genderShow.setText(sex)
        self.birthdayShow.setText(birth)
        self.favouriteNum.setText(str(fav))
        self.eatenNum.setText(str(ates))
        # TODO:设置口味，你的最爱

    def initUserEdit(self):
        database = DBOperator()
        person = database.get_person(self.account)
        name = person[0]
        nick = person[1]
        if person[3] == 0:
            sex = ''
        elif person[3] == 1:
            sex = '男'
        else:
            sex = '女'
        if person[4] != '':
            year, month, day = person[4].split('-')
        else:
            year = ''
            month = ''
            day = ''
        self.userNameEdit.setPlaceholderText(name)
        self.nickNameEdit.setPlaceholderText(nick)
        self.genderComboBox.setPlaceholderText(sex)
        self.birthday_year.setPlaceholderText(year)
        self.birthday_month.setPlaceholderText(month)
        self.birthday_day.setPlaceholderText(day)

    # 个人信息面是第一页
    def setFirstPage(self):
        self.stackedWidget.setCurrentIndex(0)

    # 编辑个人信息是第二页
    def setSecondPage(self):
        self.stackedWidget.setCurrentIndex(1)

    # 设置头像
    def setProfilePhoto(self):
        dataBase = DBOperator()
        image_pil = dataBase.get_person(self.account)[7]
        if image_pil:
            # 将PIL Image转换为QImage
            image_pil.resize((128, 128))
            image_qt = QImage(image_pil.tobytes(), image_pil.width, image_pil.height, QImage.Format_RGB888)
            image_qt.scaled(128, 128)
            # # 创建QPixmap
            pixmap = QPixmap.fromImage(image_qt)
            self.ImageLabel.setPixmap(pixmap.scaled(self.ImageLabel.width(), self.ImageLabel.height()))
            self.ImageLabel.setScaledContents(True)
            self.ImageLabel.clicked.connect(self.uploadProfilePhoto)
        else:
            pixmap = QPixmap(":/user.png")
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
            pixmap = QPixmap(file_path)
            self.ImageLabel.setPixmap(pixmap.scaled(self.ImageLabel.width(), self.ImageLabel.height()))
            # 上传图片路径到云端
            dataBase = DBOperator()
            dataBase.update_person(self.account, 'photo', file_path)
            self.createSuccessInfoBar('头像上传成功')

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
        dataBase = DBOperator()
        new_nickname = self.nickNameEdit.text()
        if self.genderComboBox.text() == '':
            new_gender = 0
        elif self.genderComboBox.text() == '男':
            new_gender = 1
        else:
            new_gender = 2
        new_birth = self.birthday_year.text() + "-" + self.birthday_month.text() + '-' + self.birthday_day.text() \
            if self.birthday_year.text() != '' else ""
        old_passwd = self.passwordEdit_old.text()
        new_passwd = self.passwordEdit_new.text()
        if old_passwd == '' and new_passwd == '':
            # 不修改密码
            if new_nickname != '':
                dataBase.update_person(self.account, 'nick', new_nickname)
                self.nickNameEdit.clear()
                self.nickNameEdit.setPlaceholderText(new_nickname)
            if new_gender != 0:
                dataBase.update_person(self.account, 'sex', new_gender)
            if new_birth != '':
                dataBase.update_person(self.account, 'birth', new_birth)
            # 然后更新用户信息界面
            self.initUserInfo()
            # 修改成功标签
            self.createSuccessInfoBar('修改成功')
        elif old_passwd != '' and new_passwd == '' or old_passwd == '' and new_passwd != '':
            self.createErrorInfoBar('请补全密码信息')
        else:
            # 首先验证原密码是否正确
            truePass = dataBase.get_person(self.account)[2]
            if truePass == old_passwd:
                dataBase.update_person(self.account, 'passwd', new_passwd)
                self.passwordEdit_old.clear()
                self.passwordEdit_new.clear()
                if new_nickname != '':
                    dataBase.update_person(self.account, 'nick', new_nickname)
                    self.nickNameEdit.clear()
                    self.nickNameEdit.setPlaceholderText(new_nickname)
                if new_gender != 0:
                    dataBase.update_person(self.account, 'sex', new_gender)
                if new_birth != '':
                    dataBase.update_person(self.account, 'birth', new_birth)
                self.createSuccessInfoBar('修改成功')
                # 然后更新用户信息界面
                self.initUserInfo()
            else:
                self.createErrorInfoBar('原密码错误')

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

    def createSuccessInfoBar(self, content):
        # convenient class mothod
        InfoBar.success(
            title='成功',
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            parent=self
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyUserWidget('xyh')
    win.show()
    sys.exit(app.exec_())
