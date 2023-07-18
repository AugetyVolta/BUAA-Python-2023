import datetime
import random

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QMessageBox
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon

from Game.MyGame import Tetris
from HomeWidget.MyHomeWidget_ui import Ui_MyHomeWidget_ui
from other import MyQWight


def getTodayDate():
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    return [int(item) for item in now.split('-')]


class MyHomeWidget(Ui_MyHomeWidget_ui, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.playGame = None
        self.setupUi(self)
        # 处理have a try
        self.setHaveATry()
        # 处理必吃榜
        self.setMustEatList()
        # 设置小游戏
        self.setGameButton()
        # 设置日历
        self.setCalendar()

    # 设置have a try
    def setHaveATry(self):
        self.MyHaveATryLabel.setAlignment(Qt.AlignCenter)
        self.tryButton.clicked.connect(self.haveATryClick)

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
        self.MyShowMealLabel.setText(s)

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
