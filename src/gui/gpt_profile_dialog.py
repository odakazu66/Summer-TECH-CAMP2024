from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, \
    QComboBox


class GPTProfileDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.id = "GPT"

        layout = QVBoxLayout()
        self.setWindowTitle("Chatbot Settings")

        name_label = QLabel("Name:")
        self.name_label_entry = QLineEdit()
        self.old_gpt_name = parent.gpt_name
        self.name_label_entry.setPlaceholderText(self.old_gpt_name)

        self.path_input = QLineEdit(self)
        self.browse_button = QPushButton("Browse...", self)
        self.browse_button.clicked.connect(self.browse_file)

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
        layout.addWidget(name_label)
        layout.addWidget(self.name_label_entry)
        layout.addWidget(self.path_input)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.voice_selection)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def browse_file(self):
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
            self.path_input.setText(file_path)
        print("new image path", self.path_input.text())

    def apply(self):
        print("Apply button clicked")

        if self.name_label_entry.text().strip() != "":
            self.parent.update_chat_names(self.id, self.old_gpt_name, self.name_label_entry.text())

        if self.path_input.text() != "":
            self.parent.update_user_icons(self.id, self.path_input.text())

        # 音声の設定
        self.parent.update_voice_selection(self.voice_selection.currentText())

        self.accept()  # Close the dialog with an accept result

    def discard(self):
        print("Discard button clicked")
        self.reject()  # Close the dialog with a reject result