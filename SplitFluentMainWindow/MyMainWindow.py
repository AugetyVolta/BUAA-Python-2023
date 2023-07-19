import qfluentwidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget
from qfluentwidgets import SplitFluentWindow, NavigationWidget, NavigationItemPosition, Theme, NavigationDisplayMode, \
    NavigationAvatarWidget, setTheme
from Game.MyGame import Tetris
from HomeWidget.MyHomeWidget import MyHomeWidget
from User.MyUser import MyUserWidget
from qfluentwidgets import FluentIcon as FIF


class MyMainWindow(SplitFluentWindow):
    def __init__(self):
        super().__init__()
        # 设置最初的主题
        self.curTheme = Theme.LIGHT
        self.setWindowTitle("The Taste Of BUAA")
        self.setWindowIcon(QIcon("{}/../picture_set/watermelon.png"))
        self.u = MyHomeWidget()
        self.addSubInterface(self.u, FIF.HOME, 'Home')

        self.user = MyUserWidget()
        self.addSubInterface(self.user, FIF.PEOPLE, 'User',
                             position=NavigationItemPosition.BOTTOM)
        self.setFixedSize(1090, 680)
        self.navigationInterface.setExpandWidth(120)
        self.navigationInterface.addItem(
            routeKey='settingInterface',
            icon=FIF.LEAF,
            text='切换主题',
            onClick=self.changeTheme,
            position=NavigationItemPosition.BOTTOM,
        )
        # 居中显示
        self.center()

    # 切换主题
    def changeTheme(self):
        if self.curTheme == Theme.LIGHT:
            setTheme(Theme.DARK)
            self.curTheme = Theme.DARK
        else:
            setTheme(Theme.LIGHT)
            self.curTheme = Theme.LIGHT

    # 窗口居中显示
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 关闭时弹窗提醒
    def closeEvent(self, event):
        reply = QMessageBox().question(self, 'Message',
                                       "Are you sure to quit?", QMessageBox.Yes |
                                       QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
