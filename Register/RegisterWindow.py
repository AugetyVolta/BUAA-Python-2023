import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import SplitTitleBar, InfoBarPosition, InfoBar
from qframelesswindow import AcrylicWindow

from Register.RegisterWindow_ui import Ui_RegisterWidget


class MyRegister(Ui_RegisterWidget, AcrylicWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setTitleBar(SplitTitleBar(self))
        self.titleBar.raise_()

        self.setWindowTitle('The Taste Of BUAA')
        self.setWindowIcon(QIcon(":/login.png"))
        # 处理注册
        self.setRegisterButton()
        self.center()

    def setRegisterButton(self):
        self.RegisterButton.clicked.connect(self.register_and_errorCatch)

    def register_and_errorCatch(self):
        # TODO:重复注册处理，差数据库是否有这个用户名

        # 信息不全处理
        if self.userName.text() == '' or self.nickName.text() == '' or self.password.text() == '' or self.password_2.text() == '':
            self.createErrorInfoBar('请补全信息')
        # 两次密码输入不统一处理
        elif self.password.text() != self.password_2.text():
            self.createErrorInfoBar('请输入相同的密码')
        # 成功注册
        else:
            # TODO:系统注册，上传服务器
            userName = self.userName.text()
            nickName = self.nickName.text()
            password = self.password.text()
            # 输出信息，恢复标签
            self.createSuccessInfoBar('恭喜你，注册成功！')
            self.userName.clear()
            self.userName.setPlaceholderText('example@example.com')
            self.nickName.clear()
            self.nickName.setPlaceholderText('Free to yourself')
            self.password.clear()
            self.password.setPlaceholderText('••••••••••••')
            self.password_2.clear()
            self.password_2.setPlaceholderText('••••••••••••')

    def center(self):
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

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
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    w = MyRegister()
    w.show()
    app.exec_()
