from PyQt5.QtWidgets import QWidget, QVBoxLayout

from FavouriteWidget.MyFavoriteWidget_ui import Ui_MyFavoriteWidget
from FavouriteWidget.test import RecursiveListWidget


class MyFavouriteWidget(Ui_MyFavoriteWidget, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.lay=QVBoxLayout()
        # self.lay.addWidget(RecursiveListWidget())
        # self.CardWidget.setLayout(self.lay)
