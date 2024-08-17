from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, \
    QComboBox


class GPTProfileDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.id = "GPT"
        self.new_icon_path = ""

        layout = QVBoxLayout()
        self.setWindowTitle("Chatbot Settings")

        self.icon_selection = QPushButton()
        self.set_icon_in_dialog(self.parent.gpt_icon_path)
        self.icon_selection.setStyleSheet("border: none;")
        self.icon_selection.setCursor(Qt.PointingHandCursor)
        self.icon_selection.clicked.connect(self.select_icon_dialog)

        name_label = QLabel("Name:")
        self.name_label_entry = QLineEdit()
        self.old_gpt_name = parent.gpt_name
        self.name_label_entry.setPlaceholderText(self.old_gpt_name)

        # 音声選択部分
        self.voice_selection = QComboBox()
        self.voice_selection.addItems(["ja-JP-Standard-A", "ja-JP-Standard-B", "ja-JP-Standard-C", "ja-JP-Standard-D"])
        self.voice_selection.setStyleSheet('QComboBox {background-color: #C0C0C0; \
                                                  height: 20px; \
                                                  border: 1px solid black;\
                                                  border-radius: 5px;} ')
        self.voice_selection.setCurrentText(self.parent.voice_thread.voice_name)

        q_buttons = QDialogButtonBox.Apply | QDialogButtonBox.Discard
        self.button_box = QDialogButtonBox(q_buttons)

        self.button_box.button(QDialogButtonBox.Apply).clicked.connect(self.apply)
        self.button_box.button(QDialogButtonBox.Discard).clicked.connect(self.discard)

        # Set up the layout
        layout.addWidget(self.icon_selection)
        layout.addWidget(name_label)
        layout.addWidget(self.name_label_entry)
        layout.addWidget(self.voice_selection)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def set_icon_in_dialog(self, icon_path):
        if icon_path != "":
            self.icon_selection.setIcon(QIcon(icon_path))
            self.icon_selection.setIconSize(QSize(50, 50))

    def select_icon_dialog(self):
        options = QFileDialog.Options()
        image_filter = "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)"
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select an Image",
            "",
            image_filter,
            options=options
        )
        if file_path:
            self.new_icon_path = file_path
        print("new image path", self.new_icon_path)
        self.set_icon_in_dialog(self.new_icon_path)

    def apply(self):
        print("Apply button clicked")

        if self.name_label_entry.text().strip() != "":
            self.parent.update_chat_names(self.id, self.old_gpt_name, self.name_label_entry.text())

        if self.new_icon_path != "":
            self.parent.update_user_icons(self.id, self.new_icon_path)

        # 音声の設定
        self.parent.update_voice_selection(self.voice_selection.currentText())

        self.accept()  # Close the dialog with an accept result

    def discard(self):
        print("Discard button clicked")
        self.reject()  # Close the dialog with a reject result