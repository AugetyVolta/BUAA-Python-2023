import sys
import ast
import time

from PyQt5 import QtGui
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QTreeWidgetItem, QListWidgetItem, QMenu, QAction
from qfluentwidgets import SubtitleLabel

from DataBase.database import DBOperator
from FavouriteWidget.MyFavoriteWidget_ui import Ui_MyFavoriteWidget
from FavouriteWidget.favouriteDishes import DishCollectionUI, BackendThread


class MyFavouriteWidget(Ui_MyFavoriteWidget, QWidget):
    def __init__(self, account):
        super().__init__()
        self.account = account
        self.setupUi(self)
        self.dishCollection = DishCollectionUI(self.account)
        # 初始化收藏夹
        self.initFavouriteList()

    def initFavouriteList(self):
        # 设置布局
        Layout_for_favouriteList = QVBoxLayout()
        favouriteListTitle = SubtitleLabel(self)
        favouriteListTitle.setText("收藏夹🎐🎐")
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        favouriteListTitle.setFont(font)
        Layout_for_favouriteList.addWidget(favouriteListTitle)
        Layout_for_favouriteList.addWidget(self.dishCollection)
        self.CardWidget_3.setLayout(Layout_for_favouriteList)
        # 设置餐厅和柜台收藏列表
        self.favouriteRestaurant.setContextMenuPolicy(3)
        self.favouriteCounter.setContextMenuPolicy(3)
        self.favouriteRestaurant.customContextMenuRequested.connect(self.showContextMenu)
        self.favouriteCounter.customContextMenuRequested.connect(self.showContextMenu_1)
        # # 初始化表的内容,从数据库读取数据
        database = DBOperator()
        if len(database.get_fav_hall(self.account)) == 0:
            self.restaurantList = []
        else:
            self.restaurantList = []
            for hall in database.get_fav_hall(self.account):
                self.restaurantList.append(hall)
        if len(database.get_fav_bar(self.account)) == 0:
            self.counterList = []
        else:
            self.counterList = []
            for bar in database.get_fav_bar(self.account):
                self.counterList.append(bar)

        self.favouriteRestaurant.addItems(self.restaurantList)
        self.favouriteCounter.addItems(self.counterList)
        self.initThread()

    def initThread(self):
        # 创建线程
        self.thread = QThread()
        self.backend = BackendThread()
        # 连接信号
        self.backend.update_date.connect(self.update)
        self.backend.moveToThread(self.thread)
        # 开始线程
        self.thread.started.connect(self.backend.run)
        self.thread.start()

    # favourite Restaurants删除设置
    def showContextMenu(self, pos):
        menu = QMenu(self)
        delete_action = QAction('删除', self)
        delete_action.triggered.connect(self.deleteItem)
        menu.addAction(delete_action)
        menu.exec_(self.favouriteRestaurant.mapToGlobal(pos))

    def deleteItem(self):
        selected_item = self.favouriteRestaurant.currentItem()
        if selected_item is not None:
            database = DBOperator()
            database.del_fav_hall(self.account, selected_item.text())
            self.favouriteRestaurant.takeItem(self.favouriteRestaurant.row(selected_item))
            # 从person的信息中删除并写回
            self.restaurantList.remove(selected_item.text())

    # favourite counters删除设置
    def showContextMenu_1(self, pos):
        menu = QMenu(self)
        delete_action = QAction('删除', self)
        delete_action.triggered.connect(self.deleteItem_1)
        menu.addAction(delete_action)
        menu.exec_(self.favouriteCounter.mapToGlobal(pos))

    def deleteItem_1(self):
        selected_item = self.favouriteCounter.currentItem()
        if selected_item is not None:
            database = DBOperator()
            database.del_fav_bar(self.account, selected_item.text())
            self.favouriteCounter.takeItem(self.favouriteCounter.row(selected_item))
            # 从person的信息中删除并写回
            self.counterList.remove(selected_item.text())

    # 一个列表加入另一个列表使用extend，不是append
    def update(self):
        database = DBOperator()
        new_list = database.get_fav_hall(self.account)
        added_elements = [x for x in new_list if x not in self.restaurantList]
        if len(added_elements) != 0:
            self.favouriteRestaurant.addItems(added_elements)
            self.restaurantList.extend(added_elements)
            added_elements.clear()
        new_list = list(database.get_fav_bar(self.account))
        added_elements = [x for x in new_list if x not in self.counterList]
        if len(added_elements) != 0:
            self.favouriteCounter.addItems(added_elements)
            self.counterList.extend(added_elements)
            added_elements.clear()
    # def closeEvent(self, event):


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyFavouriteWidget('pqy')
    window.show()
    sys.exit(app.exec_())
