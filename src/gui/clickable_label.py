from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtWidgets import QLabel


class ClickableLabel(QLabel):
    clicked = pyqtSignal(str)

    def __init__(self, id, icon_path, parent=None):
        super().__init__(parent)
        self.id = id
        self.set_icon(icon_path)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.id)

    def set_icon(self, icon_path):
        sender_pixmap = QPixmap(icon_path)
        resized_sender_pixmap = sender_pixmap.scaledToHeight(50)

        self.setPixmap(resized_sender_pixmap)

        icon_size = resized_sender_pixmap.size()
        self.setFixedSize(icon_size.width(), icon_size.height())

        self.setCursor(QCursor(Qt.PointingHandCursor))

