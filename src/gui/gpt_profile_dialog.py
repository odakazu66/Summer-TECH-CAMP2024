from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QLineEdit


class GPTProfileDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        layout = QVBoxLayout()
        self.setWindowTitle("User Settings")

        name_label = QLabel("Name:")
        self.name_label_entry = QLineEdit()
        self.name_label_entry.setPlaceholderText(parent.gpt_name)

        q_buttons = QDialogButtonBox.Apply | QDialogButtonBox.Discard
        self.button_box = QDialogButtonBox(q_buttons)

        self.button_box.button(QDialogButtonBox.Apply).clicked.connect(self.apply)
        self.button_box.button(QDialogButtonBox.Discard).clicked.connect(self.discard)

        # Set up the layout
        layout.addWidget(name_label)
        layout.addWidget(self.name_label_entry)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def apply(self):
        print("Apply button clicked")

        self.parent.set_gpt_name(self.name_label_entry.text())

        self.accept()  # Close the dialog with an accept result

    def discard(self):
        print("Discard button clicked")
        self.reject()  # Close the dialog with a reject result
