import sys
from PyQt5.QtWidgets import QWidget, QToolTip, QPushButton, QApplication, QMessageBox, QDesktopWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QCoreApplication


class MyQWight(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.i = 0

    def show_in_text(self):
        print(f"clicked {self.i}")
        self.i += 1

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')

        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.clicked.connect(self.show_in_text)
        btn.resize(btn.sizeHint())
        btn.move(50, 50)

        qbtn = QPushButton('Quit', self)
        qbtn.setToolTip("This is a <b>QuitButton</b> widget.")
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50, 100)

        self.setGeometry(300, 300, 200, 200)
        self.setWindowTitle("Icon")
        self.setWindowIcon(QIcon('../picture_set/img.png'))
        self.center()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    # 获取UIC窗口操作权限
    app = QApplication(sys.argv)
    ex = MyQWight()
    ex.show()
    sys.exit(app.exec_())
