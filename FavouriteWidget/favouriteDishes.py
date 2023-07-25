import sys

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea
from qfluentwidgets import PushButton, ScrollArea, CardWidget

from DataBase.database import DBOperator


class DishItem(QWidget):
    def __init__(self, account, dish_id):
        super().__init__()
        self.counter_name = None
        self.restaurant_name = None
        self.dish_type = None
        self.dish_name = None
        self.dish_id = dish_id
        self.account = account
        self.initUI()

    def initUI(self):
        # 连接数据库
        database = DBOperator()
        dish = database.get_dish(self.dish_id)
        layout = QHBoxLayout()
        # 菜品图像
        self.dish_image_label = QLabel(self)
        image_pil = dish[8]
        image_pil.resize((128, 128))
        image_qt = QImage(image_pil.tobytes(), image_pil.width, image_pil.height, QImage.Format_RGB888)
        image_qt.scaled(128, 128)
        pixmap = QPixmap.fromImage(image_qt)
        self.dish_image_label.setPixmap(pixmap)  # 设置菜品图片
        self.dish_image_label.setFixedSize(128, 128)
        self.dish_image_label.setScaledContents(True)
        self.dish_image_label.setStyleSheet("border: 1px solid #ccc; border-radius: 5px;")
        layout.addWidget(self.dish_image_label)

        self.dish_name = dish[1]
        if dish[2] == 4:
            self.dish_type = '早餐'
        elif dish[2] == 2:
            self.dish_type = '正餐'
        else:
            self.dish_type = '饮料'
        self.restaurant_name = dish[6]
        self.counter_name = dish[5]
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

        # 取消收藏按钮
        self.unfavorite_button = PushButton('取消收藏', self)
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

    def on_unfavorite(self):
        # 据dish_id删除一个人所收藏的菜
        database = DBOperator()
        database.del_fav_dish(self.account, self.dish_id)
        # Emit a signal to inform the parent widget to remove this item
        self.deleteLater()  # Delete the widget itself


class DishCollectionUI(QWidget):
    def __init__(self, account):
        super().__init__()
        self.account = account
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

        # 根据人的收藏添置widget
        database = DBOperator()
        for dish_id in database.get_fav_dish(self.account):
            dish_item = DishItem(dish_id=dish_id, account=self.account)
            self.dishes_layout.addWidget(dish_item)

        layout.addWidget(scroll_area)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DishCollectionUI('pqy')
    window.show()
    sys.exit(app.exec_())
