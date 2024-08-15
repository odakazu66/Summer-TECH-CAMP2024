from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog


class UserProfileDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.id = "You"
        self.old_user_name = parent.user_name

        layout = QVBoxLayout()
        self.setWindowTitle("User Settings")

        name_label = QLabel("Name:")
        self.name_label_entry = QLineEdit()
        self.name_label_entry.setPlaceholderText(self.old_user_name)

        self.path_input = QLineEdit(self)
        self.browse_button = QPushButton("Browse...", self)
        self.browse_button.clicked.connect(self.browse_file)

        q_buttons = QDialogButtonBox.Apply | QDialogButtonBox.Discard
        self.button_box = QDialogButtonBox(q_buttons)

        self.button_box.button(QDialogButtonBox.Apply).clicked.connect(self.apply)
        self.button_box.button(QDialogButtonBox.Discard).clicked.connect(self.discard)

        # Set up the layout
        layout.addWidget(name_label)
        layout.addWidget(self.name_label_entry)
        layout.addWidget(self.path_input)
        layout.addWidget(self.browse_button)
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
            self.parent.update_chat_names(self.id, self.old_user_name, self.name_label_entry.text())

        if self.path_input.text() != "":
            self.parent.update_user_icons(self.id, self.path_input.text())

        self.accept()  # Close the dialog with an accept result

    def discard(self):
        print("Discard button clicked")
        self.reject()  # Close the dialog with a reject result
