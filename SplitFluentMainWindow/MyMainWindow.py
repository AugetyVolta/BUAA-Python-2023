import qfluentwidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget
from qfluentwidgets import SplitFluentWindow, NavigationWidget, NavigationItemPosition, Theme, NavigationDisplayMode, \
    NavigationAvatarWidget, setTheme

from ManagerWidget.Manager import MyManager
from picture_set import pic_rc
from FavouriteWidget.MyFavourite import MyFavouriteWidget
from Game.MyGame import Tetris
from HistoryWidget.MyHistory import MyHistoryWidget
from HomeWidget.MyHomeWidget import MyHomeWidget
from User.MyUser import MyUserWidget
from qfluentwidgets import FluentIcon as FIF


class MyMainWindow(SplitFluentWindow):
    def __init__(self):
        super().__init__()
        # 设置最初的主题
        self.curTheme = Theme.LIGHT
        self.setWindowTitle("The Taste Of BUAA")
        self.setWindowIcon(QIcon(":/login.png"))
        self.u = MyHomeWidget()
        self.addSubInterface(self.u, FIF.HOME, 'Home')

        self.user = MyUserWidget()
        self.addSubInterface(self.user, FIF.PEOPLE, 'User',
                             position=NavigationItemPosition.BOTTOM)

        self.favourite = MyFavouriteWidget()
        self.addSubInterface(self.favourite, FIF.HEART, 'Favorite')

        self.history = MyHistoryWidget()
        self.addSubInterface(self.history, FIF.HISTORY, 'History')
        self.setFixedSize(1090, 680)
        self.navigationInterface.setExpandWidth(120)
        self.navigationInterface.addItem(
            routeKey='changeTheme',
            icon=FIF.CONSTRACT,
            text='Theme',
            onClick=self.changeTheme,
            position=NavigationItemPosition.BOTTOM,
        )
        # TODO:如果是管理员有这个功能
        self.navigationInterface.addItem(
            routeKey='manager',
            icon=FIF.LEAF,
            text='manager',
            onClick=self.change,
            position=NavigationItemPosition.BOTTOM,
        )

        # 居中显示
        self.center()

    def change(self):
        self.manager = MyManager()
        self.manager.show()

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
