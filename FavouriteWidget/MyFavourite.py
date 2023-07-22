import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QTreeWidgetItem, QListWidgetItem, QMenu, QAction
from qfluentwidgets import SubtitleLabel

from FavouriteWidget.MyFavoriteWidget_ui import Ui_MyFavoriteWidget
from FavouriteWidget.favouriteDishes import DishCollectionUI


class MyFavouriteWidget(Ui_MyFavoriteWidget, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 初始化收藏夹
        self.initFavouriteList()
        # 设置两个收藏列表
        self.favouriteRestaurant.setContextMenuPolicy(3)
        self.favouriteCounter.setContextMenuPolicy(3)
        self.favouriteRestaurant.addItems([str(i) for i in range(100)])
        self.favouriteCounter.addItems(['fad', 'daff', 'fdada', 'sdfasf'])
        self.favouriteRestaurant.customContextMenuRequested.connect(self.showContextMenu)
        self.favouriteCounter.customContextMenuRequested.connect(self.showContextMenu_1)

    def initFavouriteList(self):
        Layout_for_favouriteList = QVBoxLayout()
        favouriteListTitle = SubtitleLabel(self)
        favouriteListTitle.setText("收藏夹")
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        favouriteListTitle.setFont(font)
        Layout_for_favouriteList.addWidget(favouriteListTitle)
        Layout_for_favouriteList.addWidget(DishCollectionUI())
        self.CardWidget_3.setLayout(Layout_for_favouriteList)

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
            self.favouriteRestaurant.takeItem(self.favouriteRestaurant.row(selected_item))

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
            self.favouriteCounter.takeItem(self.favouriteCounter.row(selected_item))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyFavouriteWidget()
    window.show()
    sys.exit(app.exec_())
