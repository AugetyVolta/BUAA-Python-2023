import sys
import time

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from qfluentwidgets import SplitTitleBar, InfoBar, InfoBarPosition
from qframelesswindow import AcrylicWindow

from ManagerWidget.AddDishWidget_ui import Ui_AddDishWidget
# from ManagerWidget.Manager import MyManager
from picture_set import pic_rc


class MyAddDish(Ui_AddDishWidget, AcrylicWindow):
    def __init__(self, MyManager):
        super().__init__()
        self.MyManager = MyManager
        self.setupUi(self)
        # 设置变量
        self.dishName = None
        self.dishKind = None  # 四位2进制
        self.restaurant = None
        self.counter = None
        self.feel = None  # 0 1
        self.flavour = None  # 五位2进制

        self.setTitleBar(SplitTitleBar(self))
        self.titleBar.raise_()
        self.setWindowTitle('菜品添加')
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
        # 设置dishKindBox
        self.dishKindBox.addItems(['早餐', '中餐', '晚餐', '饮料'])
        # 连接按钮
        self.hotButton.toggled.connect(self.onRadioButtonClicked)
        self.coldButton.toggled.connect(self.onRadioButtonClicked)
        self.addDishButton.clicked.connect(self.on_commit)
        # 图像
        self.setDishImage()

    def onRadioButtonClicked(self):
        # 获取选中的单选按钮
        sender = self.sender()
        # 获取冷热
        if sender.isChecked():
            if sender.text() == '冷':
                self.feel = 0
            else:
                self.feel = 1

    def getDishKind(self):
        if self.dishKindBox.currentText() == '早餐':
            return 0b1000
        elif self.dishKindBox.currentText() == '中餐':
            return 0b0100
        elif self.dishKindBox.currentText() == '晚餐':
            return 0b0010
        elif self.dishKindBox.currentText() == '饮料':
            return 0b0001

    # 五位二进制
    def getFlavour(self):
        x_1 = 0b1 if self.CheckBox.isChecked() else 0b0
        x_2 = 0b1 if self.CheckBox_2.isChecked() else 0b0
        x_3 = 0b1 if self.CheckBox_3.isChecked() else 0b0
        x_4 = 0b1 if self.CheckBox_4.isChecked() else 0b0
        x_5 = 0b1 if self.CheckBox_5.isChecked() else 0b0
        flavour = x_1 << 4 | x_2 << 3 | x_3 << 2 | x_4 << 1 | x_5
        return flavour

    def on_commit(self):
        self.dishName = self.dishNameEdit.text()
        self.dishKind = self.getDishKind()
        self.restaurant = self.restaurantEdit.text()
        self.counter = self.counterEdit.text()
        self.flavour = self.getFlavour()
        # TODO 之后需要在这里传入数据库
        print(self.dishName)
        print(self.dishKind)
        print(self.restaurant)
        print(self.counter)
        print(self.feel)
        print(self.flavour)
        # 清空
        self.dishNameEdit.clear()
        self.dishKindBox.clear()
        self.dishKindBox.addItems(['早餐', '中餐', '晚餐', '饮料'])
        self.restaurantEdit.clear()
        self.counterEdit.clear()
        self.coldButton.setChecked(False)
        self.hotButton.setChecked(False)
        self.CheckBox.setChecked(False)
        self.CheckBox_2.setChecked(False)
        self.CheckBox_3.setChecked(False)
        self.CheckBox_4.setChecked(False)
        self.CheckBox_5.setChecked(False)
        self.createSuccessInfoBar('添加成功')
        self.MyManager.addDish_From_AddDish(self.restaurant, self.counter, self.dishName)

    def getDishInfo(self):
        return self.dishInfo

    def createSuccessInfoBar(self, content):
        # convenient class mothod
        InfoBar.success(
            title='成功',
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            parent=self
        )

    def setDishImage(self):
        pixmap = QPixmap(":/美食.png")
        self.dishImageLabel.setScaledContents(True)
        self.dishImageLabel.setPixmap(pixmap.scaled(self.dishImageLabel.width(), self.dishImageLabel.height()))
        self.dishImageLabel.clicked.connect(self.uploadProfilePhoto)

    # 更新头像
    def uploadProfilePhoto(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter('Images (*.png *.xpm *.jpg *.bmp)')
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            # 在这里执行上传头像的逻辑，这里只是简单地显示选择的图像
            pixmap = QPixmap(file_path)
            self.dishImageLabel.setScaledContents(True)
            self.dishImageLabel.setPixmap(pixmap.scaled(self.dishImageLabel.width(), self.dishImageLabel.height()))

    def center(self):
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     manager = MyAddDish(MyManager())
#     manager.show()
#     sys.exit(app.exec_())
