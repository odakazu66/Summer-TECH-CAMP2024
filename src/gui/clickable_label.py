from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QLabel


class ClickableLabel(QLabel):
    clicked = pyqtSignal(str)

    def __init__(self, id, parent=None):
        super().__init__(parent)
        self.id = id

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.id)
