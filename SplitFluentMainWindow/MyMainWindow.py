from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
from qfluentwidgets import SplitFluentWindow
from HomeWidget.MyHomeWidget import MyHomeWidget


class MyMainWindow(SplitFluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("The Taste Of BUAA")
        self.setWindowIcon(QIcon("{}/../picture_set/watermelon.png"))
        self.u = MyHomeWidget()
        self.addSubInterface(self.u, QIcon("{}/../picture_set/home.png"), 'Home')
        self.setFixedSize(1090, 680)
        self.navigationInterface.setExpandWidth(120)

    # 关闭时弹窗提醒
    def closeEvent(self, event):
        reply = QMessageBox().question(self, 'Message',
                                       "Are you sure to quit?", QMessageBox.Yes |
                                       QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
