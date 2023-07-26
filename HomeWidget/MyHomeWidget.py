import datetime
import random
import sys
import time

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QMessageBox, QHeaderView, QApplication
from PyQt5.QtCore import Qt, QDate, QObject, pyqtSignal, QThread
from PyQt5.QtGui import QIcon, QImage, QPixmap, QTransform
from qfluentwidgets import FluentIcon as FIF

from DataBase.database import DBOperator
from DishWidget.Dish import DishDetailWindow
from Game.MyGame import Tetris
from HomeWidget.MyHomeWidget_ui import Ui_MyHomeWidget_ui
from picture_set import pic_rc


# 获得今天日期List[Year, Month, Day]
def getTodayDate():
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    return [int(item) for item in now.split('-')]


class BackendThread(QObject):
    # 通过类成员对象定义信号
    update_date = pyqtSignal(int)

    # 处理业务逻辑
    def run(self):
        while 1:
            # 刷新展示页面1-3页
            for i in range(3):
                self.update_date.emit(i)
                time.sleep(3)


class MyHomeWidget(Ui_MyHomeWidget_ui, QWidget):
    def __init__(self, account, parent=None):
        super().__init__(parent=parent)
        self.backend = None
        self.thread = None
        self.playGame = None
        self.account = account
        self.ImageShow_dishId_List = []  # 滚动展示图片
        self.MushEatList_dishId = []  # 必吃榜的菜肴ID
        self.setupUi(self)
        # 处理have a try
        self.setHaveATry()
        # 处理必吃榜
        self.setMustEatList()
        # 设置小游戏
        self.setGameButton()
        # 设置日历
        self.setCalendar()
        # 设置展示界面的上下滚动展示效果
        self.initScrollShow()
        # 设置推荐列表的占满布局
        self.recommendTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 设置热门榜单

    # 处理界面的上下滚动展示效果
    def initScrollShow(self):
        # 设置显示图片和标签
        self.initScrollShowPicAndLabel()
        # 设置按钮信号
        self.PrimaryPushButton_1.clicked.connect(self.setDishShowButton_in_scroll)
        self.PrimaryPushButton_2.clicked.connect(self.setDishShowButton_in_scroll)
        self.PrimaryPushButton_3.clicked.connect(self.setDishShowButton_in_scroll)
        self.PrimaryPushButton_4.clicked.connect(self.setDishShowButton_in_scroll)
        self.PrimaryPushButton_5.clicked.connect(self.setDishShowButton_in_scroll)
        self.PrimaryPushButton_6.clicked.connect(self.setDishShowButton_in_scroll)
        self.PrimaryPushButton_7.clicked.connect(self.setDishShowButton_in_scroll)
        self.PrimaryPushButton_8.clicked.connect(self.setDishShowButton_in_scroll)
        self.PrimaryPushButton_9.clicked.connect(self.setDishShowButton_in_scroll)
        # 创建线程
        self.thread = QThread()
        self.backend = BackendThread()
        # 连接信号
        self.backend.update_date.connect(self.handleScrollShowIndex)
        self.backend.moveToThread(self.thread)
        # 开始线程
        self.thread.started.connect(self.backend.run)
        self.thread.start()

    # 滚动界面设置函数
    def handleScrollShowIndex(self, index):
        self.PopUpAniStackedWidget.setCurrentIndex(index)

    def initScrollShowPicAndLabel(self):
        # 设置菜的图片
        pixmap_1 = QPixmap("{}/../picture_set/Dishes_96x96/haha_96x96.jpg")  # 按指定路径找到图片
        pixmap_2 = QPixmap("{}/../picture_set/Dishes_96x96/红烧坤_96x96.jpg")  # 按指定路径找到图片
        pixmap_3 = QPixmap("{}/../picture_set/Dishes_96x96/九转大肠_96x96.jpg")  # 按指定路径找到图片
        pixmap_4 = QPixmap("{}/../picture_set/Dishes_96x96/红烧肉_96x96.jpg")  # 按指定路径找到图片
        self.ImageLabel_1.setPixmap(pixmap_1)
        self.ImageLabel_4.setPixmap(pixmap_2)
        self.ImageLabel_7.setPixmap(pixmap_3)
        self.ImageLabel_9.setPixmap(pixmap_4)
        self.ImageLabel_1.setScaledContents(True)
        self.ImageLabel_4.setScaledContents(True)
        self.ImageLabel_7.setScaledContents(True)
        self.ImageLabel_9.setScaledContents(True)
        # TODO:根据index设置Label

    def setDishShowButton_in_scroll(self):
        sender = self.sender()
        senderIndex = int(sender.objectName().split('_')[1]) - 1
        # TODO:根据ID显示菜肴界面
        # dishId = self.ImageShow_dishId_List[senderIndex]

    # 设置have a try
    def setHaveATry(self):
        self.MyHaveATryLabel.setAlignment(Qt.AlignCenter)
        self.tryButton.clicked.connect(self.haveATryClick)

    def setMustEatList(self):
        database = DBOperator()
        self.MushEatList_dishId = database.recommand()
        # 需要之后设置必吃榜单
        # 必吃榜设置排名数字Icon
        for i in range(self.MustEatList.count()):
            item: QtWidgets.QListWidgetItem = self.MustEatList.item(i)
            dish = database.get_dish(self.MushEatList_dishId[i])
            item.setText(dish[1])
            item.setIcon(QIcon(":/number/%d.png" % (i + 1)))
        # TODO:设置选择条目处理函数
        self.MustEatList.itemSelectionChanged.connect(self.handleMustEatListSelectionChanged)

    # 必吃榜条目选择处理函数
    def handleMustEatListSelectionChanged(self):
        # 当前的Index
        try:
            currentIndex = self.MustEatList.currentRow()
            dish_id = self.MushEatList_dishId[currentIndex]
            self.detailed_dish_window = DishDetailWindow(dish_id=dish_id, account=self.account)
            self.detailed_dish_window.show()
        except Exception as e:
            print(e)

    # have a try button处理函数
    def haveATryClick(self):
        database = DBOperator()
        Id_list = database.recommand()
        random_id = Id_list[random.randint(0, len(Id_list) - 1)]
        dish = database.get_dish(random_id)
        self.MyShowMealLabel.setText(dish[1])

    # 设置小游戏
    def setGameButton(self):
        self.relaxGameButton.setIcon(FIF.GAME)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyHomeWidget('pqy')
    win.show()
    sys.exit(app.exec_())
