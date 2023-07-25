import sys

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QLabel
from qfluentwidgets import CardWidget, PushButton

from DataBase.database import DBOperator
from HistoryWidget.HistoryItem import MyHistoryItem
from HistoryWidget.MyHistoryWidget_ui import Ui_MyHistoryWidget
from HistoryWidget.SearchForHistory import MySearchForHistory


class MyHistoryWidget(Ui_MyHistoryWidget, QWidget):
    def __init__(self, account):
        super().__init__()
        self.account = account
        self.setupUi(self)
        # 设置一个专门的item_list
        self.item_list = []
        # 创建一个QWidget用于放置菜品项
        self.dishes_widget = CardWidget()
        self.dishes_layout = QVBoxLayout()
        self.dishes_widget.setLayout(self.dishes_layout)
        # 将QWidget设置为滚动区域的小部件
        self.scroll_area.setWidget(self.dishes_widget)

        # 根据人的历史设置表项
        database = DBOperator()
        history = database.get_ates(self.account)
        for dish_id, time in history:
            dish_item = MyHistoryItem(dish_id=dish_id,
                                      time=time,
                                      account=self.account,
                                      item_list=self.item_list)
            # 根据dishID布置菜
            self.dishes_layout.addWidget(dish_item)
            # 加入item_list中
            self.item_list.append(dish_item)

        self.searchButton.clicked.connect(self.search_items)
        self.clearButton.clicked.connect(self.clear_items)

    def search_items(self):
        self.search = MySearchForHistory(self.item_list)
        self.search.show()

    def clear_items(self):
        print(self.item_list)
        for item in self.item_list:
            item.delete_history(flag=False)
        self.item_list.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyHistoryWidget('pqy')
    window.show()
    sys.exit(app.exec_())
