import sys

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication

from FavouriteWidget.MyFavoriteWidget_ui import Ui_MyFavoriteWidget
from FavouriteWidget.favouriteDishes import DishCollectionUI


class MyFavouriteWidget(Ui_MyFavoriteWidget, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        Lay = QVBoxLayout()
        Lay.addWidget(DishCollectionUI())
        self.CardWidget_3.setLayout(Lay)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyFavouriteWidget()
    window.show()
    sys.exit(app.exec_())
