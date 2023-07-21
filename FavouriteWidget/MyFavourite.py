import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication
from qfluentwidgets import SubtitleLabel

from FavouriteWidget.MyFavoriteWidget_ui import Ui_MyFavoriteWidget
from FavouriteWidget.favouriteDishes import DishCollectionUI


class MyFavouriteWidget(Ui_MyFavoriteWidget, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        Lay = QVBoxLayout()
        favouriteListTitle = SubtitleLabel(self)
        favouriteListTitle.setText("收藏夹")
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        favouriteListTitle.setFont(font)
        Lay.addWidget(favouriteListTitle)
        Lay.addWidget(DishCollectionUI())
        self.CardWidget_3.setLayout(Lay)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyFavouriteWidget()
    window.show()
    sys.exit(app.exec_())
