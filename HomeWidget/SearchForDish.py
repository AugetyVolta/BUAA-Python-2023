import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QHeaderView, QTableWidgetItem, QApplication

from DataBase.database import DBOperator
from DishWidget.Dish import DishDetailWindow
from SearchWidget.SearchWidget_ui import Ui_SearchWidget
from picture_set import pic_rc


class MySearchForDish(Ui_SearchWidget, QWidget):
    def __init__(self, account, search_content):
        super().__init__()
        self.setupUi(self)
        self.account = account
        self.objectBase = []  # 对象仓库
        self.search_dishId_List = []  # 搜索结果Id表
        self.setWindowTitle('搜索')
        self.setWindowIcon(QIcon(':/login.png'))
        self.TableWidget.removeColumn(3)
        self.TableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.SearchLineEdit.searchButton.clicked.connect(self.show_search_result)
        # 设置一开始搜索的界面
        self.init_search_result(search_content)

    def init_search_result(self, search_content):
        if search_content != '':
            database = DBOperator()
            dish_id_list = database.search(search_content)
            self.search_dishId_List = dish_id_list
            for dish_id in dish_id_list:
                dish = database.get_dish(dish_id)
                self.addTableRow([dish[1], dish[6], dish[5]])
        self.TableWidget.itemSelectionChanged.connect(self.handleSearchSelectionChanged)

    def show_search_result(self):
        # 清空上次记录
        self.TableWidget.setRowCount(0)
        search_content = self.SearchLineEdit.text()
        if search_content != '':
            database = DBOperator()
            dish_id_list = database.search(search_content)
            self.search_dishId_List = dish_id_list
            for dish_id in dish_id_list:
                dish = database.get_dish(dish_id)
                self.addTableRow([dish[1], dish[6], dish[5]])

    def addTableRow(self, data):
        row_count = self.TableWidget.rowCount()
        self.TableWidget.insertRow(row_count)
        for col, value in enumerate(data):
            item = QTableWidgetItem(value)
            self.TableWidget.setItem(row_count, col, item)

    # 条目处理函数
    def handleSearchSelectionChanged(self):
        currentIndex = self.TableWidget.currentRow()
        dish_id = self.search_dishId_List[currentIndex]
        search_item_window = DishDetailWindow(dish_id=dish_id, account=self.account)
        self.objectBase.append(search_item_window)
        search_item_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MySearchForDish('pqy', '清炒')
    win.show()
    sys.exit(app.exec_())
