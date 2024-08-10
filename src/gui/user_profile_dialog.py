from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout


class UserProfileDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.setWindowTitle("User Settings")

        q_buttons = QDialogButtonBox.Apply | QDialogButtonBox.Discard
        self.button_box = QDialogButtonBox(q_buttons)

        self.button_box.button(QDialogButtonBox.Apply).clicked.connect(self.apply)
        self.button_box.button(QDialogButtonBox.Discard).clicked.connect(self.discard)

        # Set up the layout
        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def apply(self):
        print("Apply button clicked")
        self.accept()  # Close the dialog with an accept result

    def discard(self):
        print("Discard button clicked")
        self.reject()  # Close the dialog with a reject result
