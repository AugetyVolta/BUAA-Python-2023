import sys

import qfluentwidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget, QApplication
from qfluentwidgets import SplitFluentWindow, NavigationWidget, NavigationItemPosition, Theme, NavigationDisplayMode, \
    NavigationAvatarWidget, setTheme

from ManagerWidget.Manager import MyManager
from picture_set import pic_rc
from FavouriteWidget.MyFavourite import MyFavouriteWidget
from HistoryWidget.MyHistory import MyHistoryWidget
from HomeWidget.MyHomeWidget import MyHomeWidget
from User.MyUser import MyUserWidget
from qfluentwidgets import FluentIcon as FIF


class MyMainWindow(SplitFluentWindow):
    def __init__(self, account):
        super().__init__()
        # 设置大小
        self.manager = None
        self.setFixedSize(1090, 680)
        self.navigationInterface.setExpandWidth(120)
        # 当前的账户
        self.account = account
        self.ManagerAccount = ['pqy', 'zby', 'hyk', 'ygf', 'manager']  # 管理员账户
        manager_access = (self.account in self.ManagerAccount)
        # 设置最初的主题
        self.curTheme = Theme.LIGHT
        self.setWindowTitle("The Taste Of BUAA")
        self.setWindowIcon(QIcon(":/login.png"))
        # 添加主界面
        self.u = MyHomeWidget(self.account)
        self.addSubInterface(self.u, FIF.HOME, 'Home')
        # 添加用户界面
        self.userWidget = MyUserWidget(self.account)
        self.addSubInterface(self.userWidget, FIF.PEOPLE, 'User',
                             position=NavigationItemPosition.BOTTOM)
        # 添加收藏界面
        self.favourite = MyFavouriteWidget(self.account)
        self.addSubInterface(self.favourite, FIF.HEART, 'Favorite')
        # 添加历史记录界面
        self.history = MyHistoryWidget(self.account)
        self.addSubInterface(self.history, FIF.HISTORY, 'History')
        # 添加主题切换按钮
        self.navigationInterface.addItem(
            routeKey='changeTheme',
            icon=FIF.CONSTRACT,
            text='Theme',
            onClick=self.changeTheme,
            position=NavigationItemPosition.BOTTOM,

        )
        # 如果是管理员设置管理菜肴的界面
        if manager_access:
            self.navigationInterface.addItem(
                routeKey='manager',
                icon=FIF.EDIT,
                text='manager',
                onClick=self.open_manager_window,
                position=NavigationItemPosition.BOTTOM,
            )
        # 居中显示
        self.center()

    def open_manager_window(self):
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyMainWindow('pqy')
    win.show()
    sys.exit(app.exec_())
