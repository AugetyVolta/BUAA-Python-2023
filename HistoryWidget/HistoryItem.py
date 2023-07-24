from PyQt5.QtWidgets import QWidget

from HistoryWidget.History_item_ui import Ui_History_item


class MyHistoryItem(Ui_History_item, QWidget):
    def __init__(self, dish_name, dish_type, restaurant_name, counter_name):
        super().__init__()
        self.setupUi(self)

        self.dish_name.setText(dish_name)
        self.dish_type.setText(dish_type)
        self.restaurant_name.setText(restaurant_name)
        self.counter_name.setText(counter_name)
        # 设置固定大小
        self.setFixedSize(820, 135)
