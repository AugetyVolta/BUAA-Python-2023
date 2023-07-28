import datetime
import random
import sys
import time

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QMessageBox, QHeaderView, QApplication, QTableWidgetItem
from PyQt5.QtCore import Qt, QDate, QObject, pyqtSignal, QThread
from PyQt5.QtGui import QIcon, QImage, QPixmap, QTransform
from qfluentwidgets import FluentIcon as FIF

from DataBase.database import DBOperator
from DishWidget.Dish import DishDetailWindow
from Game.MyGame import Tetris
from HomeWidget.MyHomeWidget_ui import Ui_MyHomeWidget_ui
from HomeWidget.SearchForDish import MySearchForDish
from picture_set import pic_rc


# 获得今天日期List[Year, Month, Day]
def getTodayDate():
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    return [int(item) for item in now.split('-')]


class BackendThread(QObject):
    # 滚动roll效果
    update_date = pyqtSignal(int)
    # 更新必吃榜 5min更新一次
    update_must_list = pyqtSignal()
    # 更新滚动推荐 30min更新一次
    update_roll = pyqtSignal()
    # 更新热门榜单 1h更新一次
    update_hot_list = pyqtSignal()

    # 处理业务逻辑
    def run(self):
        timer = 0
        while 1:
            # 刷新展示页面1-3页
            for i in range(3):
                self.update_date.emit(i)
                time.sleep(5)
                timer += 1
                if (timer % 60) == 0:
                    self.update_must_list.emit()
                if (timer % 360) == 0:
                    self.update_roll.emit()
                if (timer % 720) == 0:
                    self.update_hot_list.emit()
                    timer = 0


class MyHomeWidget(Ui_MyHomeWidget_ui, QWidget):
    def __init__(self, account, parent=None):
        super().__init__()
        self.searchWindow = None
        self.dish_roll_item = None
        self.setupUi(self)
        self.detailed_dish_window = None
        self.backend = None
        self.thread = None
        self.playGame = None
        self.account = account
        self.objectBase = []  # 用来放对象
        self.ImageShow_dishId_List = []  # 滚动展示图片
        self.MushEatList_dishId = []  # 必吃榜的菜肴ID
        self.HotList_dishId = []  # 热门榜单的菜肴ID
        self.dishNameShowLabels = [self.dishNameLable_1, self.BodyLabel_2, self.BodyLabel_3, self.BodyLabel_4,
                                   self.BodyLabel_5, self.BodyLabel_6, self.BodyLabel_7, self.BodyLabel_8,
                                   self.BodyLabel_9]
        self.primaryButtons = [self.PrimaryPushButton_1, self.PrimaryPushButton_2, self.PrimaryPushButton_3,
                               self.PrimaryPushButton_4, self.PrimaryPushButton_5,
                               self.PrimaryPushButton_6, self.PrimaryPushButton_7, self.PrimaryPushButton_8,
                               self.PrimaryPushButton_9]
        self.ImageLabels = [self.ImageLabel_1, self.ImageLabel_2, self.ImageLabel_3, self.ImageLabel_4,
                            self.ImageLabel_5, self.ImageLabel_6, self.ImageLabel_7, self.ImageLabel_8,
                            self.ImageLabel_9]
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
        self.setHotList()
        # 设置搜索按钮触发
        self.MySearchLineEdit.searchButton.clicked.connect(self.Search)
        # 设置热榜的条目选择函数
        self.recommendTable.itemSelectionChanged.connect(self.handleHotListSelectionChanged)

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
        self.backend.update_must_list.connect(self.updateMustEatList)
        self.backend.update_roll.connect(self.initScrollShowPicAndLabel)
        self.backend.update_hot_list.connect(self.setHotList)
        self.backend.moveToThread(self.thread)
        # 开始线程
        self.thread.started.connect(self.backend.run)
        self.thread.start()

    # 滚动界面设置函数
    def handleScrollShowIndex(self, index):
        self.PopUpAniStackedWidget.setCurrentIndex(index)

    # 初始化滚动界面
    def initScrollShowPicAndLabel(self):
        # 根据index设置show 界面
        database = DBOperator()
        self.ImageShow_dishId_List = database.personalized_recommendation(self.account)
        for i in range(9):
            dish = database.get_dish(self.ImageShow_dishId_List[i])
            self.dishNameShowLabels[i].setText(dish[1])
            image_pil = dish[8]
            image_pil.resize((96, 96))
            image_qt = QImage(image_pil.tobytes(), image_pil.width, image_pil.height, QImage.Format_RGB888)
            image_qt.scaled(96, 96)
            pixmap = QPixmap.fromImage(image_qt)
            self.ImageLabels[i].setPixmap(pixmap)
            self.ImageLabels[i].setFixedSize(96, 96)
            self.ImageLabels[i].setScaledContents(True)

    # 每一个按键的触发函数
    def setDishShowButton_in_scroll(self):
        sender = self.sender()
        senderIndex = int(sender.objectName().split('_')[1]) - 1
        # 根据ID显示菜肴界面
        dish_id = self.ImageShow_dishId_List[senderIndex]
        dish_roll_item = DishDetailWindow(account=self.account, dish_id=dish_id)
        self.objectBase.append(dish_roll_item)
        dish_roll_item.show()
        # self.dish_roll_item = DishDetailWindow(account=self.account, dish_id=dish_id)
        # self.dish_roll_item.show()

    # 设置have a try
    def setHaveATry(self):
        self.MyHaveATryLabel.setAlignment(Qt.AlignCenter)
        self.tryButton.clicked.connect(self.haveATryClick)

    # 设置必吃榜
    def setMustEatList(self):
        database = DBOperator()
        self.MushEatList_dishId = database.recommend()
        # 需要之后设置必吃榜单
        # 必吃榜设置排名数字Icon
        for i in range(self.MustEatList.count()):
            item: QtWidgets.QListWidgetItem = self.MustEatList.item(i)
            dish = database.get_dish(self.MushEatList_dishId[i])
            item.setText(dish[1])
            item.setIcon(QIcon(":/number/%d.png" % (i + 1)))
        # 设置选择条目处理函数
        self.MustEatList.itemSelectionChanged.connect(self.handleMustEatListSelectionChanged)

    # 必吃榜条目选择处理函数
    def handleMustEatListSelectionChanged(self):
        # 当前的Index
        try:
            currentIndex = self.MustEatList.currentRow()
            dish_id = self.MushEatList_dishId[currentIndex]
            detailed_dish_window = DishDetailWindow(dish_id=dish_id, account=self.account)
            self.objectBase.append(detailed_dish_window)
            detailed_dish_window.show()
            # self.detailed_dish_window = DishDetailWindow(dish_id=dish_id, account=self.account)
            # self.detailed_dish_window.show()
        except Exception as e:
            print(e)

    # have a try button处理函数
    def haveATryClick(self):
        database = DBOperator()
        Id_list = database.recommend()
        random_id = Id_list[random.randint(0, len(Id_list) - 1)]
        dish = database.get_dish(random_id)
        self.MyShowMealLabel.setText(dish[1])

    # 设置热门榜单
    def setHotList(self):
        database = DBOperator()
        dish_id_weight = database.get_popularity(50)
        # 清空recommendList
        self.recommendTable.setRowCount(0)
        # 清空HotList_dishId
        self.HotList_dishId.clear()
        i = 0
        for dish_id, weight in dish_id_weight:
            dish = database.get_dish(dish_id)
            if i < len(dish_id_weight) * 0.2:
                heart_flag = '💖💖💖💖💖'
            elif i < len(dish_id_weight) * 0.4:
                heart_flag = '💖💖💖💖️'
            elif i < len(dish_id_weight) * 0.6:
                heart_flag = '💖💖💖'
            elif i < len(dish_id_weight) * 0.8:
                heart_flag = '💖💖'
            else:
                heart_flag = '💖️'
            self.addTableRow([dish[1], dish[6], dish[5], heart_flag])
            self.HotList_dishId.append(dish_id)
            i += 1

    # 热榜条目点击函数
    def handleHotListSelectionChanged(self):
        currentIndex = self.recommendTable.currentRow()
        dish_id = self.HotList_dishId[currentIndex]
        hotList_window = DishDetailWindow(dish_id=dish_id, account=self.account)
        self.objectBase.append(hotList_window)
        hotList_window.show()

    # Table增加行函数
    def addTableRow(self, data):
        row_count = self.recommendTable.rowCount()
        self.recommendTable.insertRow(row_count)
        for col, value in enumerate(data):
            item = QTableWidgetItem(value)
            item.setTextAlignment(Qt.AlignCenter)
            self.recommendTable.setItem(row_count, col, item)

    # 搜索函数
    def Search(self):
        search_content = self.MySearchLineEdit.text()
        self.MySearchLineEdit.clear()
        self.searchWindow = MySearchForDish(self.account, search_content)
        self.searchWindow.show()

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

    # 更新必吃榜单
    def updateMustEatList(self):
        database = DBOperator()
        self.MushEatList_dishId = database.recommend()
        # 必吃榜设置排名数字Icon
        for i in range(self.MustEatList.count()):
            item: QtWidgets.QListWidgetItem = self.MustEatList.item(i)
            dish = database.get_dish(self.MushEatList_dishId[i])
            item.setText(dish[1])
            item.setIcon(QIcon(":/number/%d.png" % (i + 1)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyHomeWidget('pqy')
    win.show()
    sys.exit(app.exec_())
