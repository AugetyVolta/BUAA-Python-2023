from PyQt5.QtWidgets import QWidget

from HistoryWidget.MyHistoryWidget_ui import Ui_MyHistoryWidget


class MyHistoryWidget(Ui_MyHistoryWidget, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
