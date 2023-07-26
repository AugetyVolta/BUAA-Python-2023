import sys
import time

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QThread
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QLabel
from qfluentwidgets import CardWidget, PushButton

from DataBase.database import DBOperator
from HistoryWidget.HistoryItem import MyHistoryItem
from HistoryWidget.MyHistoryWidget_ui import Ui_MyHistoryWidget
from HistoryWidget.SearchForHistory import MySearchForHistory


class BackendThread(QObject):
    # 通过类成员对象定义信号
    update_date = pyqtSignal()

    # 处理业务逻辑
    def run(self):
        while 1:
            # 刷新1-10
            for i in range(1, 11):
                self.update_date.emit()
                time.sleep(5)


class MyHistoryWidget(Ui_MyHistoryWidget, QWidget):
    def __init__(self, account):
        super().__init__()
        self.backend = None
        self.thread = None
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
        self.initThread()

    def search_items(self):
        self.search = MySearchForHistory(self.item_list)
        self.search.show()

    def clear_items(self):
        for item in self.item_list:
            item.delete()
        self.item_list.clear()

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

    def update(self):
        database = DBOperator()
        list_old = [[item.dish_id, item.time] for item in self.item_list]
        list_new = [[dish_id, time] for dish_id, time in database.get_ates(self.account)]
        add_elements = [x for x in list_new if x not in list_old]
        if len(add_elements) != 0:
            add_items = [MyHistoryItem(dish_id=dish_id,
                                       time=time,
                                       account=self.account,
                                       item_list=self.item_list) for [dish_id, time] in add_elements]
            self.item_list.extend(add_items)
            for item in add_items:
                self.dishes_layout.addWidget(item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyHistoryWidget('pqy')
    window.show()
    sys.exit(app.exec_())
