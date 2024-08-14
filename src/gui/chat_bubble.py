from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame, QLabel

from .clickable_label import ClickableLabel
from .gpt_profile_dialog import GPTProfileDialog
from .user_profile_dialog import UserProfileDialog


class ChatBubble(QHBoxLayout):
    def __init__(self, sender_id, message, parent):
        super().__init__()
        self.parent_window = parent
        self.sender_id = sender_id
        self.message = message

        if self.sender_id == "You":
            self.sender_name = self.parent_window.user_name
            self.icon_path = self.parent_window.user_icon_path
        else:
            self.sender_name = self.parent_window.gpt_name
            self.icon_path = self.parent_window.gpt_icon_path

        self.init_ui()

    def init_ui(self):

        bubble = QFrame()
        bubble.setObjectName("bubble_frame")
        bubble_layout = QVBoxLayout(bubble)

        sender_label = QLabel(self.sender_name)
        sender_label.setFont(QFont("メイリオ", 10, QFont.Bold))
        sender_label.setStyleSheet("color: gray;")  # 名前の色

        bubble_label = QLabel(self.message)
        bubble_label.setWordWrap(True)
        bubble_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        bubble_label.setCursor(Qt.IBeamCursor)
        bubble_label.setFont(QFont("メイリオ", 12))
        bubble_label.setStyleSheet("color: black; background-color: {}; border-radius: 15px; padding: 10px;".format('#E0F7FA' if self.sender_id == "You" else '#E1FFC7'))

        bubble_layout.addWidget(sender_label)
        bubble_layout.addWidget(bubble_label)
        bubble_layout.addStretch(1)

        sender_icon = ClickableLabel(self.sender_name, self.icon_path)
        sender_icon.clicked.connect(self.on_icon_clicked)

        if self.sender_id == "You":
            bubble.setStyleSheet("margin: 0px 0px 0px 100px;")
            self.addWidget(bubble)
            self.addWidget(sender_icon, alignment=Qt.AlignVCenter)
        else:
            bubble.setStyleSheet("margin: 0px 100px 0px 0px;")
            self.addWidget(sender_icon, alignment=Qt.AlignVCenter)
            self.addWidget(bubble)

    def on_icon_clicked(self):
        print(f"{self.sender_id}'s icon was clicked")

        if self.sender_id == "You":
            dialog = UserProfileDialog(parent=self.parent_window)
        else:
            dialog = GPTProfileDialog(parent=self.parent_window)

        result = dialog.exec()
        if result:
            print("Applied New Settings.")
        else:
            print("Discarded New Settings.")

    def set_sender(self, new_name):
        pass

    def set_icon_path(self, new_path):
        pass










