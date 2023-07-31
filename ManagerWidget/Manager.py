import ast
import os
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QInputDialog, QWidget
from qfluentwidgets import SplitTitleBar, InfoBar, InfoBarPosition
from qframelesswindow import AcrylicWindow

from DataBase.database import DBOperator
from ManagerWidget.AddDish import MyAddDish
from ManagerWidget.ManagerWindow_ui import Ui_ManagerWidget
from picture_set import pic_rc


class MyManager(Ui_ManagerWidget, AcrylicWindow):
    def __init__(self):
        super().__init__()
        self.addDishWidget = None
        self.dic = None
        self.setupUi(self)
        # 初始化图信息
        self.init_dish_graph()

        self.setTitleBar(SplitTitleBar(self))
        self.titleBar.raise_()
        self.setWindowTitle('菜品信息管理')
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

        self.center()
        # 连接按钮
        self.addRestaurantButton.clicked.connect(self.addRestaurant)
        self.addCounterButton.clicked.connect(self.addCounter)
        self.addDishButton.clicked.connect(self.addDish)
        self.deleteButton.clicked.connect(self.deleteItem)

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

    def addRestaurant_by_String(self, restaurant):
        if not (restaurant in self.dic):
            self.dic.setdefault(restaurant, {})

    def addCounter_by_String(self, restaurant, counter):
        self.addRestaurant_by_String(restaurant)
        if not (counter in self.dic[restaurant]):
            self.dic[restaurant].setdefault(counter, [])

    def addDish_by_String(self, restaurant, counter, dish):
        self.addCounter_by_String(restaurant, counter)
        if not (dish in self.dic[restaurant][counter]):
            self.dic[restaurant][counter].append(dish)

    def addRestaurant(self):
        restaurant_name, ok = QtWidgets.QInputDialog.getText(
            self.ManagerWidget, "Add Restaurant", "Enter the name of the restaurant:"
        )
        if ok and restaurant_name:
            restaurant_item = QtWidgets.QTreeWidgetItem(self.resturantWidget)
            restaurant_item.setText(0, restaurant_name)
            self.addRestaurant_by_String(restaurant_name)
            graph = str(self.dic)
            database = DBOperator()
            dst_graph = '"' + graph + '"'
            database.execute(f'update globe set total = {dst_graph};')
        self.resturantWidget.expandAll()

    def addCounter(self):
        selected_item = self.resturantWidget.currentItem()
        if selected_item and not selected_item.parent():
            counter_name, ok = QtWidgets.QInputDialog.getText(
                self.ManagerWidget, "Add Counter", "Enter the name of the counter:"
            )
            if ok and counter_name:
                counter_item = QtWidgets.QTreeWidgetItem(selected_item)
                counter_item.setText(0, counter_name)
                self.addCounter_by_String(selected_item.text(0), counter_name)
                graph = str(self.dic)
                database = DBOperator()
                dst_graph = '"' + graph + '"'
                database.execute(f'update globe set total = {dst_graph};')
        self.resturantWidget.expandAll()

    def addDish(self):
        selected_item = self.resturantWidget.currentItem()
        # 如果制定了餐厅
        # if selected_item and selected_item.parent():
        #     dish_name, ok = QInputDialog.getText(
        #         self.ManagerWidget, "Add Dish", "Enter the name of the dish:"
        #     )
        #     if ok and dish_name:
        #         dish_item = QtWidgets.QTreeWidgetItem(selected_item)
        #         dish_item.setText(0, dish_name)
        #         self.addDish_by_String(selected_item.parent().text(0), selected_item.text(0), dish_name)
        # else:
        # 如果没有指定餐厅，跳转增加菜的页面
        self.addDishWidget = MyAddDish(self)
        self.addDishWidget.show()
        self.resturantWidget.expandAll()

    def addDish_From_AddDish(self, restaurant, counter, dishName, imagePath):
        found_items = self.resturantWidget.findItems(restaurant, Qt.MatchExactly)
        if not found_items:
            restaurant_item = QtWidgets.QTreeWidgetItem(self.resturantWidget)
            restaurant_item.setText(0, restaurant)
        else:
            restaurant_item = found_items[0]

        found_items = self.searchSubItems(restaurant_item, counter)
        if not found_items:
            counter_item = QtWidgets.QTreeWidgetItem(restaurant_item)
            counter_item.setText(0, counter)
        else:
            counter_item = found_items[0]

        found_items = self.searchSubItems(counter_item, dishName)
        if not found_items:
            dish_item = QtWidgets.QTreeWidgetItem(counter_item)
            dish_item.setText(0, dishName)
        else:
            dish_item = found_items[0]
        self.addDish_by_String(restaurant, counter, dishName)
        graph = str(self.dic)
        database = DBOperator()
        dst_graph = '"' + graph + '"'
        database.execute(f'update globe set total = {dst_graph};')
        self.resturantWidget.expandAll()

    def searchSubItems(self, parent_item, search_text):
        found_items = self.resturantWidget.findItems(search_text, Qt.MatchExactly | Qt.MatchRecursive)
        return [item for item in found_items if item.parent() == parent_item]

    def deleteItem(self):
        database = DBOperator()
        selected_item = self.resturantWidget.currentItem()
        if selected_item:
            parent_item = selected_item.parent()
            if parent_item:
                parent_parent_item = parent_item.parent()
                if parent_parent_item:  # 说明就是直接是菜
                    # 删除treeWidget中的项
                    parent_item.removeChild(selected_item)
                    # 删除大字符串中的菜
                    self.dic[parent_parent_item.text(0)][parent_item.text(0)].remove(selected_item.text(0))
                    # 删除总的菜单中的菜
                    dish_id = database.get_id(selected_item.text(0), parent_item.text(0), parent_parent_item.text(0))
                    database.del_dish(dish_id)
                else:  # 说明是柜台
                    parent_item.removeChild(selected_item)
                    # 删除大字符串中的柜台
                    self.dic[parent_item.text(0)].pop(selected_item.text(0))
                    # 将他的孩子(菜)也一块删除,递归删除
                    try:
                        self.deleteCounter(parent_item.text(0), selected_item.text(0))
                    except Exception as e:
                        print(e)

            else:
                index = self.resturantWidget.indexOfTopLevelItem(selected_item)
                self.resturantWidget.takeTopLevelItem(index)
                # 删除大字符串中的餐厅
                self.dic.pop(selected_item.text(0))
                # 递归删除餐馆里所有的菜
                self.deleteRestaurant(selected_item.text(0))
            graph = str(self.dic)
            database = DBOperator()
            dst_graph = '"' + graph + '"'
            database.execute(f'update globe set total = {dst_graph};')

    # 删除柜台里的所有菜
    def deleteCounter(self, restaurant_name, counter_name):
        database = DBOperator()
        id_list = database.get_all_id()
        for Id in id_list:
            dish_counter = database.get_dish(Id)[5]
            dish_restaurant = database.get_dish(Id)[6]
            if dish_counter == counter_name and dish_restaurant == restaurant_name:
                database.del_dish(Id)

    # 删除餐厅里的所有菜
    def deleteRestaurant(self, restaurant_name):
        database = DBOperator()
        id_list = database.get_all_id()
        for Id in id_list:
            dish_restaurant = database.get_dish(Id)[6]
            if dish_restaurant == restaurant_name:
                database.del_dish(Id)

    def center(self):
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def closeEvent(self, event):
        graph = str(self.dic)
        f = open('dict', 'w+')
        f.write(graph)
        database = DBOperator()
        dst_graph = '"' + graph + '"'
        database.execute(f'update globe set total = {dst_graph};')


    # def test(self):
    #     database = DBOperator()
    #     id_list = database.get_all_id()
    #     self.dic = {}
    #     for Id in id_list:
    #         dish = database.get_dish(Id)
    #         self.addDish_From_AddDish(dish[6], dish[5], dish[1], None)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    manager = MyManager()
    manager.show()
    sys.exit(app.exec_())
