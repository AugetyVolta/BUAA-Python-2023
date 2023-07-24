import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QListWidget, QVBoxLayout, QHBoxLayout, QWidget, \
    QFrame, QListWidgetItem
from PyQt5 import QtCore, QtGui
from qfluentwidgets import SubtitleLabel, ScrollArea, CardWidget

from HistoryWidget.MyHistoryWidget_ui import Ui_MyHistoryWidget
from SearchWidget.MySearchWidget_ui import Ui_SearchWidget
from HistoryWidget.HistoryDishes import DishItem

class MyHistoryWidget(QMainWindow, Ui_MyHistoryWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 初始化历史记录
        self.initHistoryList()

        # 连接按钮点击事件
        self.pushButton.clicked.connect(self.show_search_widget)
        self.pushButton_2.clicked.connect(self.clear_history)

        # 创建搜索界面并添加到stackedWidget
        self.search_widget = QWidget()
        self.search_ui = Ui_SearchWidget()
        self.search_ui.setupUi(self.search_widget)
        self.stackedWidget.addWidget(self.search_widget)


    def show_search_widget(self):
        # 切换到搜索界面
        self.stackedWidget.setCurrentWidget(self.search_widget)

    def clear_history(self):
        # 清空历史记录的逻辑
        self.listWidget.clear()

    def initHistoryList(self):
        # 将Scroll Area的内容设置为listWidget
        for i in range(10):
            dish_item = DishItem(dish_name=f'鱼香肉丝{i + 1}',
                                 dish_type='类型A',
                                 restaurant_name='餐厅A',
                                 counter_name='柜台A')
            list_item = QListWidgetItem(self.listWidget)
            self.listWidget.setItemWidget(list_item, dish_item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyHistoryWidget()
    window.show()
    sys.exit(app.exec_())
