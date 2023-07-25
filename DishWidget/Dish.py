import os
import sys
import ast

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QTextEdit, QPushButton, QWidget, \
    QScrollArea, QHBoxLayout, QDesktopWidget
from qfluentwidgets import TextEdit, CaptionLabel, StrongBodyLabel, PrimaryPushButton, PushButton, BodyLabel, \
    ScrollArea, ImageLabel, SplitTitleBar, SubtitleLabel
from qframelesswindow import AcrylicWindow
from picture_set import pic_rc


class DishDetailWindow(AcrylicWindow):
    # TODO:需要传入菜的id,以及人的Id
    def __init__(self, dish_name, dish_type, restaurant_name, counter_name, account):
        super().__init__()
        self.setTitleBar(SplitTitleBar(self))
        self.titleBar.raise_()
        self.setWindowIcon(QIcon(":/login.png"))
        self.windowEffect.setMicaEffect(self.winId(), isDarkMode=False)
        self.titleBar.titleLabel.setStyleSheet("""
                            QLabel{
                                background: transparent;
                                font: 18px '微软雅黑';
                                padding: 0 4px;
                                color: black
                            }
                """)
        self.dish_name = dish_name
        self.dish_type = dish_type
        self.restaurant_name = restaurant_name
        self.counter_name = counter_name

        if not os.path.exists("list") or os.path.getsize("list") == 0:
            self.comments = []
        else:
            f = open("list", "r")
            self.comments = ast.literal_eval(f.readline())  # 用于存储评论的列表
        self.reply_to_user = None  # 用于存储被回复用户的信息

        self.initUI()

    def initUI(self):
        self.setWindowTitle('菜品详情页面')
        self.setGeometry(100, 100, 600, 900)
        self.center()

        # 菜品详情显示区域
        # 设置菜品图像 必须是128*128的图片
        self.dish_image_lable = ImageLabel(None)
        self.dish_image_lable.setGeometry(QtCore.QRect(190, 170, 128, 128))
        pixmap = QPixmap("../picture_set/tmp/九转大肠.jpg")
        self.dish_image_lable.setPixmap(pixmap)
        self.dish_image_lable.setScaledContents(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dish_image_lable.sizePolicy().hasHeightForWidth())
        self.dish_image_lable.setSizePolicy(sizePolicy)
        self.dish_image_lable.setMinimumSize(QtCore.QSize(128, 128))
        self.dish_image_lable.setMaximumSize(QtCore.QSize(128, 128))
        # 设置菜品详细信息
        dish_info_label = QLabel(f'菜名：{self.dish_name}\n'
                                 f'类型：{self.dish_type}\n'
                                 f'餐厅：{self.restaurant_name}\n'
                                 f'柜台：{self.counter_name}')
        dish_info_label.setStyleSheet("font-size: 24px;")

        # 收藏和吃过的按钮
        self.favorite_button = PushButton('收藏')
        self.favorite_button.setFixedSize(90, 45)
        self.favorite_button.setStyleSheet(
            "font-size: 20px; "
            "background-color: #3ac1ff; "
            "color: white; border: none; "
            "border-radius: 5px; "
            "padding: 10px 20px;")

        self.eaten_button = PushButton('吃过')
        self.eaten_button.setFixedSize(90, 45)
        self.eaten_button.setStyleSheet(
            "font-size: 20px; "
            "background-color: #ff9d8c; "
            "color: white; border: none; "
            "border-radius: 5px; "
            "padding: 10px 20px;")

        # 收藏和吃过按钮布局
        self.favorite_eaten_layout = QVBoxLayout()
        self.favorite_eaten_layout.addWidget(self.favorite_button)
        self.favorite_eaten_layout.addWidget(self.eaten_button)
        self.favorite_eaten_layout.setSpacing(5)  # 设置按钮之间的间距

        # 菜品图片，菜品信息，收藏和吃过按钮的布局
        self.dish_infoAndButton_layout = QHBoxLayout()
        self.dish_infoAndButton_layout.addWidget(self.dish_image_lable)
        self.dish_infoAndButton_layout.addWidget(dish_info_label)
        self.dish_infoAndButton_layout.addLayout(self.favorite_eaten_layout)

        # 收藏餐厅和收藏柜台按钮
        self.favorite_restaurant = PushButton('收藏餐厅')
        self.favorite_counter = PushButton('收藏柜台')
        self.favorite_restaurant.setStyleSheet(
            "font-size: 20px; "
            "background-color: #b0a6ff; "
            "color: white; border: none; "
            "border-radius: 5px; "
            "padding: 5px 10px;")
        self.favorite_counter.setStyleSheet(
            "font-size: 20px; "
            "background-color: #b0a6ff; "
            "color: white; border: none; "
            "border-radius: 5px; "
            "padding: 5px 10px;")

        # 收藏餐厅和收藏柜台按钮的布局
        self.layout_for_restuarant_counter = QHBoxLayout()
        self.layout_for_restuarant_counter.addWidget(self.favorite_restaurant)
        self.layout_for_restuarant_counter.addWidget(self.favorite_counter)

        # 创建QScrollArea用于显示评论
        self.scroll_area = ScrollArea()
        self.scroll_area.setWidgetResizable(True)  # 设置滚动区域的小部件可以调整大小

        # 创建一个QWidget用于放置评论项
        self.comments_widget = QWidget()
        self.comments_layout = QVBoxLayout()
        self.comments_widget.setLayout(self.comments_layout)

        # 将QWidget设置为滚动区域的小部件
        self.scroll_area.setWidget(self.comments_widget)

        # 评论区域
        self.comment_label = BodyLabel('评论：')
        self.comment_label.setStyleSheet("font-size: 24px;")
        self.comment_edit = TextEdit()
        self.comment_edit.setPlaceholderText('在这里输入您的评论...')
        self.comment_edit.setStyleSheet("font-size: 20px;")
        self.submit_button = PushButton('提交评论')
        self.submit_button.setStyleSheet(
            "font-size: 20px; "
            "background-color: #5baf4c; "
            "color: white; border: none; "
            "border-radius: 5px; "
            "padding: 10px 20px;")
        self.clear_button = PushButton('清空评论')
        self.clear_button.setStyleSheet(
            "font-size: 20px; "
            "background-color: #f44336; "
            "color: white; border: none; "
            "border-radius: 5px; "
            "padding: 10px 20px;")

        # 安排布局
        layout = QVBoxLayout()
        layout_for_button = QHBoxLayout()
        layout.addItem(QtWidgets.QSpacerItem(20, 60))
        layout.addLayout(self.dish_infoAndButton_layout)
        layout.addLayout(self.layout_for_restuarant_counter)
        layout.addWidget(self.comment_label)
        layout.addWidget(self.comment_edit)
        layout_for_button.addWidget(self.submit_button)
        layout_for_button.addWidget(self.clear_button)
        layout.addLayout(layout_for_button)
        layout.addWidget(self.scroll_area)  # 将QScrollArea添加到布局中

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setLayout(layout)
        # 连接按钮的点击事件
        self.submit_button.clicked.connect(self.on_submit)
        self.clear_button.clicked.connect(self.on_clear)
        self.favorite_restaurant.clicked.connect(self.set_restaurant_button)
        self.favorite_counter.clicked.connect(self.set_counter_button)
        self.favorite_button.clicked.connect(self.set_favourite_button)
        self.eaten_button.clicked.connect(self.set_eaten_button)

        # 显示暂无评论的提示
        self.no_comment_label = QLabel('暂无评论')
        self.no_comment_label.setStyleSheet("font-size: 24px; color: gray; margin: 10px;")

        # 初始时没有评论，添加暂无评论的提示
        self.comments_layout.addWidget(self.no_comment_label)

        # 如果原来有评论就更新评论
        self.update_comments()

        self.setStyleSheet("""
                    QPushButton {
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        padding: 10px 20px;
                        font-size: 20px;
                    }

                    QPushButton:hover {
                        background-color: #45a049;
                        cursor: pointer;
                    }

                    QTextEdit {
                        border: 1px solid gray;
                        padding: 5px;
                    }

                    QLabel.comment {
                        background-color: #f0f0f0;
                        padding: 10px;
                        border: 1px solid #ccc;
                        border-radius: 5px;
                    }
                """)

    def on_submit(self):
        # 获取用户输入的评论内容
        username = '匿名用户'  # 这里可以进一步实现用户登录获取用户名
        comment_text = self.comment_edit.toPlainText()

        # 添加评论到列表
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        self.comments.insert(0, {'username': username, 'comment': comment_text, 'time': current_time,
                                 'reply_to': self.reply_to_user})  # 将新评论插入到列表的第一个位置

        # 刷新评论区域
        self.update_comments()

        # 清空输入框
        self.comment_edit.clear()

        # 重置被回复用户信息
        self.reply_to_user = None
        self.comment_edit.setPlaceholderText('在这里输入您的评论...')

    def on_clear(self):
        # 清空输入框
        self.comment_edit.clear()
        # 重置被回复用户信息
        self.reply_to_user = None
        self.comment_edit.setPlaceholderText('在这里输入您的评论...')

    def reply_to_comment(self, reply_user):
        # 设置回复框可见，并显示被回复用户的信息
        self.reply_to_user = reply_user
        self.comment_edit.setPlaceholderText(f'回复 {reply_user}:')
        self.comment_edit.setFocus()

    def update_comments(self):
        # 清空评论区域内容
        for i in reversed(range(self.comments_layout.count())):
            self.comments_layout.itemAt(i).widget().setParent(None)

        if not self.comments:
            # 如果没有评论，显示暂无评论的提示
            self.comments_layout.addWidget(self.no_comment_label)
        else:
            # 移除暂无评论的提示
            self.no_comment_label.setParent(None)

            # 更新评论区域内容
            for comment in self.comments:
                comment_text = f"{comment['username']}：{comment['comment']}  <font color='gray'>({comment['time']})</font>"
                if comment['reply_to']:
                    comment_text = f"{comment['username']} 回复 {comment['reply_to']}：{comment['comment']}  <font color='gray'>({comment['time']})</font>"
                comment_label = QLabel(comment_text)
                comment_label.setObjectName('comment')  # 设置样式名称

                # 设置评论标签的点击事件
                comment_label.mousePressEvent = lambda event, u=comment['username']: self.reply_to_comment(u)

                self.comments_layout.addWidget(comment_label)

        # 滚动到评论显示框的顶部
        scroll_bar = self.scroll_area.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.minimum())

    # TODO:设置dish界面四个收藏按钮函数
    # 收藏菜
    def set_favourite_button(self):
        pass

    # 吃过
    def set_eaten_button(self):
        pass

    # 收藏餐厅
    def set_restaurant_button(self):
        pass

    # 收藏柜台
    def set_counter_button(self):
        pass

    def closeEvent(self, event):
        store_file = open("list", "w+")
        store_file.write(str(self.comments))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 在这里传入菜肴信息
    window = DishDetailWindow(dish_name='九转大肠',
                              dish_type='中餐',
                              restaurant_name='小胖餐厅',
                              counter_name='保留原味柜台',
                              account=None)
    window.show()
    sys.exit(app.exec_())
