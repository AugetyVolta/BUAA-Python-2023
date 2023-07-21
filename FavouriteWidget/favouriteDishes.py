import sys

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea
from qfluentwidgets import ScrollArea, PushButton, CardWidget


class DishItem(QWidget):
    def __init__(self, dish_name, dish_type, restaurant_name, counter_name):
        super().__init__()
        self.dish_name = dish_name
        self.dish_type = dish_type
        self.restaurant_name = restaurant_name
        self.counter_name = counter_name

        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()

        # 菜品图像
        self.dish_image_label = QLabel(self)
        # 设置菜品图像，您可以根据实际情况设置菜品图片
        pixmap = QPixmap('../picture_set/BUAA.jpg')
        self.dish_image_label.setPixmap(pixmap)  # 设置菜品图片
        self.dish_image_label.setFixedSize(128, 128)
        self.dish_image_label.setScaledContents(True)
        self.dish_image_label.setStyleSheet("border: 1px solid #ccc; border-radius: 5px;")
        layout.addWidget(self.dish_image_label)

        # 菜品信息
        dish_info_label = QLabel(f'菜名：{self.dish_name}\n'
                                 f'类型：{self.dish_type}\n'
                                 f'餐厅：{self.restaurant_name}\n'
                                 f'柜台：{self.counter_name}')
        dish_info_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(dish_info_label)

        # 收藏按钮
        self.favorite_button = PushButton('收藏', self)
        self.favorite_button.setStyleSheet(
            "font-size: 14px; background-color: #E0C240; color: white; border: none; border-radius: 5px; padding: 5px 10px;")
        layout.addWidget(self.favorite_button, alignment=QtCore.Qt.AlignRight)

        self.setLayout(layout)


class DishCollectionUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('菜品收藏')
        self.setGeometry(100, 100, 600, 400)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 创建一个滚动区域来放置菜品列表
        scroll_area = ScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # 创建一个QWidget用于放置菜品项
        self.dishes_widget = CardWidget()
        self.dishes_layout = QVBoxLayout()
        self.dishes_widget.setLayout(self.dishes_layout)

        # 将QWidget设置为滚动区域的小部件
        scroll_area.setWidget(self.dishes_widget)

        # 示例：添加三个菜品项
        for i in range(10):
            dish_item = DishItem(dish_name=f'菜品{i + 1}',
                                 dish_type='类型A',
                                 restaurant_name='餐厅A',
                                 counter_name='柜台A')
            self.dishes_layout.addWidget(dish_item)

        layout.addWidget(scroll_area)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DishCollectionUI()
    window.show()
    sys.exit(app.exec_())
