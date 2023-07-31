import sys

from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QInputDialog

from DataBase.database import DBOperator
from HistoryWidget.History_item_ui import Ui_History_item


class MyHistoryItem(Ui_History_item, QWidget):
    def __init__(self, account, dish_id, time, item_list):
        super().__init__()
        self.setupUi(self)
        self.account = account
        self.dish_id = dish_id
        self.time = time
        self.item_list = item_list
        database = DBOperator()
        dish = database.get_dish(self.dish_id)
        dish_name = dish[1]
        if dish[2] == 4:
            dish_type = '早餐'
        elif dish[2] == 2:
            dish_type = '正餐'
        else:
            dish_type = '饮料'
        restaurant_name = dish[6]
        counter_name = dish[5]
        self.dish_name.setText(dish_name)
        self.dish_type.setText(dish_type)
        self.restaurant_name.setText(restaurant_name)
        self.counter_name.setText(counter_name)
        self.history_time.setText(time)
        # 设置图片
        image_pil = dish[8]
        image_pil.resize((96, 96))
        image_qt = QImage(image_pil.tobytes(), image_pil.width, image_pil.height, QImage.Format_RGB888)
        image_qt.scaled(96, 96)
        pixmap = QPixmap.fromImage(image_qt)
        self.ImageLabel.setPixmap(pixmap)  # 设置菜品图片
        self.ImageLabel.setFixedSize(96, 96)
        self.ImageLabel.setScaledContents(True)
        self.ImageLabel.setStyleSheet("border: 1px solid #ccc; border-radius: 5px;")
        # 设置固定大小
        self.setFixedSize(820, 135)
        # 设置删除按钮
        self.deleteButton.clicked.connect(self.delete_history)
        self.history_time.mousePressEvent = self.on_item_click

    def delete_history(self):
        for item in self.item_list:
            if item.time == self.time and item.dish_id == self.dish_id:
                self.item_list.remove(item)
        # 根据传入的personId删掉这条历史
        database = DBOperator()
        database.del_ates(self.account, self.dish_id, self.time)
        self.deleteLater()

    def delete(self):
        # 根据传入的personId删掉这条历史
        database = DBOperator()
        database.del_ates(self.account, self.dish_id, self.time)
        self.deleteLater()

    def on_item_click(self, evnet):
        old = self.history_time.text()
        time, ok = QInputDialog.getText(
            self, "Change Time", "Enter the new time(yyyy-MM-dd HH:mm:ss):", text=old
        )
        if time and ok:
            database = DBOperator()
            tmp = time.split('\n')
            time = tmp[0] + '\n' + tmp[1]
            self.time = time
            self.history_time.setText(time)
            database.update_ates(self.account, self.dish_id, old, time)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyHistoryItem(account='pyq', dish_id=5, time='2023-7-10', item_list=[])
    win.show()
    sys.exit(app.exec_())
