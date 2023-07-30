import ast
import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import SplitTitleBar
from qframelesswindow import AcrylicWindow

from DataBase.database import DBOperator
from DishWidget.Dish import DishDetailWindow
from UserDishWidget.userWindow_ui import Ui_userWidget
from picture_set import pic_rc


class MyUser(Ui_userWidget, AcrylicWindow):
    def __init__(self, account):
        super().__init__()
        self.addDishWidget = None
        self.dic = None
        self.account = account
        self.setupUi(self)
        self.objectBase = []
        # 初始化图信息
        self.init_dish_graph()
        # 初始化菜总数
        self.init_dish_num()
        self.setTitleBar(SplitTitleBar(self))
        self.titleBar.raise_()
        self.setWindowTitle('菜品信息查看')
        self.setWindowIcon(QIcon(":/login.png"))
        self.windowEffect.setMicaEffect(self.winId(), isDarkMode=False)
        self.titleBar.titleLabel.setStyleSheet("""
                                            QLabel{
                                                background: transparent;
                                                font: 14px '微软雅黑';
                                                padding: 0 4px;
                                                color: black
                                            }
                                """)

        self.PrimaryPushButton.clicked.connect(self.seeInfo)
        self.center()

    def init_dish_graph(self):
        database = DBOperator()
        dish_graph = database.execute('select * from globe;')
        if dish_graph[0][0] == '':
            self.dic = {}
        else:
            self.dic = dict(ast.literal_eval(dish_graph[0][0]))
            for key in self.dic.keys():
                restaurant_item = QtWidgets.QTreeWidgetItem(self.resturantWidget)
                restaurant_item.setText(0, key)
                for key_1 in self.dic[key].keys():
                    counter_item = QtWidgets.QTreeWidgetItem(restaurant_item)
                    counter_item.setText(0, key_1)
                    for dish in self.dic[key][key_1]:
                        dish_item = QtWidgets.QTreeWidgetItem(counter_item)
                        dish_item.setText(0, dish)
            self.resturantWidget.expandAll()

    # 初始化菜总数
    def init_dish_num(self):
        database = DBOperator()
        cnt = len(database.get_all_id())
        self.BodyLabel.setText(f' 总数：{cnt}')

    # 菜品详情
    def seeInfo(self):
        database = DBOperator()
        selected_item = self.resturantWidget.currentItem()
        if selected_item:
            parent_item = selected_item.parent()
            if parent_item:
                parent_parent_item = parent_item.parent()
                # 说明就是直接是菜
                if parent_parent_item:
                    # 得到菜的id
                    dish_id = database.get_id(selected_item.text(0), parent_item.text(0), parent_parent_item.text(0))
                    dish_window = DishDetailWindow(dish_id=dish_id, account=self.account)
                    self.objectBase.append(dish_window)
                    dish_window.show()

    def center(self):
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    manager = MyUser(account='user_X')
    manager.show()
    sys.exit(app.exec_())
