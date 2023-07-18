import sys
from MainWindow.myWindow import *
from picture_set import *
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())
