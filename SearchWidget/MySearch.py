import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget

from SearchWidget.MySearchWidget_ui import Ui_SearchWidget

class SearchWidget(QWidget, Ui_SearchWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.searchButton.clicked.connect(self.search)

    def search(self):
        # 在这里执行搜索逻辑，假设我们有一个名为"search"的函数来获取搜索结果
        keyword = self.searchLineEdit.text()
        results = self.search(keyword)

        # 清空列表并添加搜索结果
        self.resultListWidget.clear()
        self.resultListWidget.addItems(results)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 创建搜索界面并显示
    search_widget = SearchWidget()
    search_widget.show()

    sys.exit(app.exec_())