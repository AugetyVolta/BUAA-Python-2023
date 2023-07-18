import datetime
import random

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDesktopWidget
from PyQt5.QtCore import Qt, QDate

from Game.MyGame import Tetris
from MainWindow.MyWindow_ui import Ui_MyWindow_ui
from other import MyQWight


def getTodayDate():
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    return [int(item) for item in now.split('-')]


class MyWindow(QMainWindow, Ui_MyWindow_ui):
    def __init__(self):
        super().__init__()
        self.Mywidget = None
        self.playGame = None
        self.setupUi(self)
        self.statusBar().show()
        # TODO:设置MainWindow的title和icon
        self.setWindowTitle("The Taste Of BUAA")
        self.setWindowIcon(QIcon("{}/../picture_set/img.png"))
        # TODO:处理have a try
        self.setHaveATry()
        # TODO:处理必吃榜
        self.setMustEatList()
        # 设置小游戏
        self.setGameButton()
        # 设置日历
        self.setCalendar()

    # 设置have a try
    def setHaveATry(self):
        self.showLabel.setAlignment(Qt.AlignCenter)
        self.tryButton.clicked.connect(self.haveATryClick)

    # 设置必吃榜
    def setMustEatList(self):
        # 必吃榜设置排名数字Icon
        for i in range(self.MustEatList.count()):
            item: QtWidgets.QListWidgetItem = self.MustEatList.item(i)
            item.setStatusTip("name")
            item.setIcon(QIcon("{}/../picture_set/number/%d.png" % (i + 1)))
        # TODO:需要之后设置必吃榜单

        # TODO:设置选择条目处理函数
        self.MustEatList.itemSelectionChanged.connect(self.handleMustEatListSelectionChanged)

    # 必吃榜条目选择处理函数
    def handleMustEatListSelectionChanged(self):
        currentItem = self.MustEatList.currentItem()
        print(currentItem.text())
        self.Mywidget = MyQWight.MyQWight()
        self.Mywidget.show()

    # have a try button处理函数
    def haveATryClick(self):
        s = str(random.randint(1, 1000))
        self.showLabel.setText(s)

    # 设置小游戏
    def setGameButton(self):
        self.relaxGameButton.setIcon(QIcon("{}/../picture_set/game.png"))
        self.relaxGameButton.clicked.connect(self.openGameWindow)

    # 打开游戏窗口
    def openGameWindow(self):
        self.relaxGameButton.setEnabled(False)
        self.playGame = Tetris()
        self.relaxGameButton.setEnabled(True)

    # 设置日历
    def setCalendar(self):
        date = QDate(*getTodayDate())
        self.MyCalendarPicker.setDate(date)

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
