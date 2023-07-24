import sys

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea
from qfluentwidgets import PushButton, ScrollArea, CardWidget


class DishItem(QWidget):
    def __init__(self, dish_name, dish_type, restaurant_name, counter_name):
        super().__init__()
        self.dish_name = dish_name
        self.dish_type = dish_type
        self.restaurant_name = restaurant_name
        self.counter_name = counter_name

        self.initUI()

    def on_unfavorite(self):
            # Emit a signal to inform the parent widget to remove this item
            self.deleteLater()  # Delete the widget itself

    def initUI(self):
        layout = QHBoxLayout()

        # 菜品图像
        self.dish_image_label = QLabel(self)
        # 设置菜品图像，您可以根据实际情况设置菜品图片
        pixmap = QPixmap('{}/../picture_set/BUAA.jpg')
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
        # 设置菜品标签样式
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        dish_info_label.setFont(font)

        layout.addWidget(dish_info_label)

        # 删除历史按钮
        self.unfavorite_button = PushButton('删除历史', self)
        self.unfavorite_button.setStyleSheet(
            "font-size: 16px; background-color: #FF4500; color: white; border: none; border-radius: 5px; padding: 5px 10px;")
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.unfavorite_button.setFont(font)
        layout.addWidget(self.unfavorite_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)

        # 设置背景色样式
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f8f8;
                border: 0px solid #ccc;
                border-radius: 5px;
            }
        """)

        # 连接取消收藏按钮点击事件
        self.unfavorite_button.clicked.connect(self.on_unfavorite)

