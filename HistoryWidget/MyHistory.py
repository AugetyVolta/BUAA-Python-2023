import sys

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QLabel
from qfluentwidgets import CardWidget, PushButton

from HistoryWidget.HistoryItem import MyHistoryItem
from HistoryWidget.MyHistoryWidget_ui import Ui_MyHistoryWidget


class MyHistoryWidget(Ui_MyHistoryWidget, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 创建一个QWidget用于放置菜品项
        self.dishes_widget = CardWidget()
        self.dishes_layout = QVBoxLayout()
        self.dishes_widget.setLayout(self.dishes_layout)
        # 将QWidget设置为滚动区域的小部件
        self.scroll_area.setWidget(self.dishes_widget)

        # TODO:根据人的收藏添置widget
        # 设置菜品图像，您可以根据实际情况设置菜品图片
        pixmap = QPixmap('{}/../picture_set/BUAA.jpg')
        for i in range(10):
            dish_item = MyHistoryItem(dish_name='鱼香肉丝',
                                      dish_type='类型A',
                                      restaurant_name='餐厅A',
                                      counter_name='柜台A')
            # dish_id=None,
            # pixmap=pixmap)  # TODO 根据dishID布置菜
            self.dishes_layout.addWidget(dish_item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyHistoryWidget()
    window.show()
    sys.exit(app.exec_())
