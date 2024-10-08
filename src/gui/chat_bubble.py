import qtawesome as qta
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame, QLabel, QPushButton

from .clickable_label import ClickableLabel
from .gpt_profile_dialog import GPTProfileDialog
from .user_profile_dialog import UserProfileDialog
from modules.playback import PlaybackThread


class ChatBubble(QHBoxLayout):
    def __init__(self, sender_id, message, parent, sound_path=None):
        super().__init__()
        self.parent_window = parent
        self.sender_id = sender_id
        self.message = message
        self.sound_path = sound_path

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
        bubble_label.setStyleSheet("""color: black; 
        background-color: {}; 
        border-radius: 15px; 
        padding: 10px;""".format('#E1FFC7' if self.sender_id == "You" else '#E0F7FA'))

        bubble_layout.addWidget(sender_label)
        if self.sender_id == "You":
            bubble_layout.setAlignment(sender_label, Qt.AlignRight)
        else:
            bubble_layout.setAlignment(sender_label, Qt.AlignLeft)

        bubble_layout.addWidget(bubble_label)
        bubble_layout.addStretch(1)

        if self.sound_path is not None:
            # bottom layout to hold play button
            bottom_layout = QHBoxLayout()

            play_icon = qta.icon("fa5.play-circle")
            self.play_button = QPushButton(play_icon, "")
            self.play_button.setIconSize(QSize(20, 20))
            self.play_button.setStyleSheet("border: none;")
            self.play_button.setCursor(Qt.PointingHandCursor)

            self.play_button.setStyleSheet(
                """
                QPushButton {
                    background-color: #B3E5FC;  /* Light blue color */
                    border: none;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #81D4FA;  /* Slightly darker blue on hover */
                }
                """
            )
            self.playback_thread = None
            self.play_button.clicked.connect(self.play_or_stop)

            sender_icon = ClickableLabel(self.sender_name, self.icon_path)
            sender_icon.clicked.connect(self.on_icon_clicked)

            if self.sender_id == "You":
                bubble.setStyleSheet("QFrame { padding: 0px 0px 0px 100px;}")
                bottom_layout.addStretch(1)
                bottom_layout.addWidget(self.play_button)
                bubble_layout.addLayout(bottom_layout)
                self.addWidget(bubble)
                self.addWidget(sender_icon, alignment=Qt.AlignVCenter)
            else:
                bubble.setStyleSheet("QFrame { padding: 0px 100px 0px 0px;}")
                bottom_layout.addWidget(self.play_button)
                bottom_layout.addStretch(1)
                bubble_layout.addLayout(bottom_layout)
                self.addWidget(sender_icon, alignment=Qt.AlignVCenter)
                self.addWidget(bubble)
        else:
            sender_icon = ClickableLabel(self.sender_name, self.icon_path)
            sender_icon.clicked.connect(self.on_icon_clicked)

            if self.sender_id == "You":
                bubble.setStyleSheet("QFrame { padding: 0px 0px 0px 100px; }")
                self.addWidget(bubble)
                self.addWidget(sender_icon, alignment=Qt.AlignVCenter)
            else:
                bubble.setStyleSheet("QFrame { padding: 0px 100px 0px 0px; }")
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

    def play_or_stop(self):
        if self.playback_thread is None:  # Play
            filename = self.sound_path  # Replace with your file
            self.playback_thread = PlaybackThread(filename)
            self.playback_thread.finished.connect(self.on_playback_finished)
            self.playback_thread.start()

            stop_icon = qta.icon("fa5.stop-circle")
            self.play_button.setIcon(stop_icon)
        else:  # Stop
            self.playback_thread.stop_playback()
            self.playback_thread.wait()  # Ensure the thread stops before resetting
            self.playback_thread = None

            play_icon = qta.icon("fa5.play-circle")
            self.play_button.setIcon(play_icon)

    def on_playback_finished(self):
        self.playback_thread = None
        play_icon = qta.icon("fa5.play-circle")
        self.play_button.setIcon(play_icon)

    def set_sender(self, new_name):
        pass

    def set_icon_path(self, new_path):
        pass










