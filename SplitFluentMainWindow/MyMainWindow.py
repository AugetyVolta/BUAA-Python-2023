from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget
from qfluentwidgets import SplitFluentWindow, NavigationWidget, NavigationItemPosition, Theme, NavigationDisplayMode, \
    NavigationAvatarWidget, setTheme
from Game.MyGame import Tetris
from HomeWidget.MyHomeWidget import MyHomeWidget
from other.MyQWight import MyQWight
from other.findMain import FindAndReplaceDlg


class MyMainWindow(SplitFluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("The Taste Of BUAA")
        self.setWindowIcon(QIcon("{}/../picture_set/watermelon.png"))
        self.u = MyHomeWidget()
        self.addSubInterface(self.u, QIcon("{}/../picture_set/home.png"), 'Home')
        # self.win = FindAndReplaceDlg("1231415413")
        # self.addSubInterface(self.win, QIcon("{}/../picture_set/like.png"), 'subHome')
        self.setFixedSize(1090, 680)
        self.navigationInterface.setExpandWidth(120)
        # self.navigationInterface.addWidget(
        #     routeKey='avatar',
        #     widget=self.u,
        #     position=NavigationItemPosition.BOTTOM
        # )
        # self.navigationInterface
        # 居中显示
        self.center()

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
