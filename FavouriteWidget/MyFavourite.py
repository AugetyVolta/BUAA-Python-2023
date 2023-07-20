from PyQt5.QtWidgets import QWidget

from FavouriteWidget.MyFavoriteWidget_ui import Ui_MyFavoriteWidget


class MyFavouriteWidget(Ui_MyFavoriteWidget, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
