from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QHeaderView, QTableWidgetItem
from picture_set import pic_rc
from SearchWidget.SearchWidget_ui import Ui_SearchWidget


class MySearchForHistory(Ui_SearchWidget, QWidget):
    def __init__(self, source_list):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('历史查询')
        self.setWindowIcon(QIcon(':/login.png'))
        self.source_list = source_list
        self.TableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.SearchLineEdit.searchButton.clicked.connect(self.show_search_result)

    def show_search_result(self):
        # 清空上次记录
        self.TableWidget.setRowCount(0)
        try:
            search_content = self.SearchLineEdit.text()
            if search_content != '':
                for item in self.source_list:
                    if search_content in item.dish_name.text() or \
                            search_content in item.restaurant_name.text() or \
                            search_content in item.counter_name.text() or \
                            search_content in item.history_time.text():
                        self.addTableRow([item.dish_name.text(), item.restaurant_name.text(), item.counter_name.text(),
                                          item.history_time.text()])
        except Exception as e:
            print(e)

    def addTableRow(self, data):
        row_count = self.TableWidget.rowCount()
        self.TableWidget.insertRow(row_count)
        for col, value in enumerate(data):
            item = QTableWidgetItem(value)
            self.TableWidget.setItem(row_count, col, item)
