from PyQt5.QtWidgets import QWidget

from HistoryWidget.History_item_ui import Ui_History_item


class MyHistoryItem(Ui_History_item, QWidget):
    def __init__(self, dish_name, dish_type, restaurant_name, counter_name, history_time, person_id, pixmap):
        super().__init__()
        self.setupUi(self)

        self.dish_name.setText(dish_name)
        self.dish_type.setText(dish_type)
        self.restaurant_name.setText(restaurant_name)
        self.counter_name.setText(counter_name)
        self.history_time.setText(history_time)
        # 设置固定大小
        self.setFixedSize(820, 135)
        # 设置删除按钮
        self.deleteButton.clicked.connect(self.delete_history)

    def delete_history(self):
        self.deleteLater()
        # TODO:根据传入的personId删掉这条历史
