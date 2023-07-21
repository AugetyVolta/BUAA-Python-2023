import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QWidget
from qfluentwidgets import SplitTitleBar, setThemeColor
from qframelesswindow import AcrylicWindow

from Login.LoginWindow_ui import Ui_LoginWidget
from Register.RegisterWindow import MyRegister
from SplitFluentMainWindow.MyMainWindow import MyMainWindow


class MyLogin(Ui_LoginWidget, AcrylicWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(701, 534)

        self.setTitleBar(SplitTitleBar(self))
        self.titleBar.raise_()

        self.setWindowTitle('The Taste Of BUAA')
        self.setWindowIcon(QIcon(":/login.png"))

        self.windowEffect.setMicaEffect(self.winId(), isDarkMode=False)
        self.setStyleSheet("LoginWindow{background: rgba(242, 242, 242, 0.8)}")
        self.titleBar.titleLabel.setStyleSheet("""
                    QLabel{
                        background: transparent;
                        font: 13px 'Segoe UI';
                        padding: 0 4px;
                        color: white
                    }
        """)
        # 设置登录跳转
        self.setLoginButton()
        # 设置注册跳转
        self.setRegisterButton()
        self.center()

    def setLoginButton(self):
        self.LoginButton.clicked.connect(self.go_to_mainWindow)

    def setRegisterButton(self):
        self.RegisterButton.clicked.connect(self.go_to_register)

    def go_to_mainWindow(self):
        MainWindow = MyMainWindow()
        MainWindow.show()
        self.close()

    def go_to_register(self):
        registerWindow = MyRegister()
        registerWindow.show()

    def center(self):
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    w = MyLogin()
    w.show()
    app.exec_()
