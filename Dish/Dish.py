import os
import sys
import ast
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QTextEdit, QPushButton, QWidget, \
    QScrollArea, QHBoxLayout, QDesktopWidget
from qfluentwidgets import TextEdit, CaptionLabel, StrongBodyLabel, PrimaryPushButton, PushButton, BodyLabel, ScrollArea


class DishDetailWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        if not os.path.exists("list") or os.path.getsize("list") == 0:
            self.comments = []
        else:
            f = open("list", "r")
            self.comments = ast.literal_eval(f.readline())  # 用于存储评论的列表
        self.reply_to_user = None  # 用于存储被回复用户的信息

        self.initUI()

    def initUI(self):
        self.setWindowTitle('菜品详情页面')
        self.setGeometry(100, 100, 300, 900)
        self.center()

        # 菜品详情显示区域
        self.dish_detail_label = QLabel('菜品名称：鱼香肉丝\n菜品简介：这是一道经典的川菜，口味鲜美，适合大众口味。')
        self.dish_detail_label.setStyleSheet("font-size: 24px;")

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
        self.submit_button.setStyleSheet("font-size: 20px;")
        self.clear_button = PushButton('清空评论')
        self.clear_button.setStyleSheet("font-size: 20px;")

        # 安排布局
        layout = QVBoxLayout()
        layout_for_button = QHBoxLayout()
        layout.addWidget(self.dish_detail_label)
        layout.addWidget(self.comment_label)
        layout.addWidget(self.comment_edit)
        layout_for_button.addWidget(self.submit_button)
        layout_for_button.addWidget(self.clear_button)
        layout.addLayout(layout_for_button)
        layout.addWidget(self.scroll_area)  # 将QScrollArea添加到布局中

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        # 连接按钮的点击事件
        self.submit_button.clicked.connect(self.on_submit)
        self.clear_button.clicked.connect(self.on_clear)

        # 显示暂无评论的提示
        self.no_comment_label = QLabel('暂无评论')
        self.no_comment_label.setStyleSheet("font-size: 24px; color: gray; margin: 10px;")

        # 初始时没有评论，添加暂无评论的提示
        self.comments_layout.addWidget(self.no_comment_label)

        # 如果原来有评论就更新评论
        self.update_comments()

        self.setStyleSheet("""
                    PushButton {
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        padding: 10px 20px;
                        font-size: 20px;
                    }

                    PushButton:hover {
                        background-color: #45a049;
                        cursor: pointer;
                    }

                    TextEdit {
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
    window = DishDetailWindow()
    window.show()
    sys.exit(app.exec_())