from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import Qt

class ScrollareaWithBackground(QScrollArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bg_pixmap = None  # Initially no background image

    def setBackgroundImage(self, bg_path):
        # Load and scale the pixmap to the size of the scroll area
        self.bg_pixmap = QPixmap(bg_path).scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.viewport().update()  # Trigger a repaint to show the background

    def clearBackgroundImage(self):
        # Clear the background image
        self.bg_pixmap = None
        self.viewport().update()  # Trigger a repaint to remove the background

    def paintEvent(self, event):
        painter = QPainter(self.viewport())

        if self.bg_pixmap:
            # Draw the pixmap if it is set
            painter.drawPixmap(0, 0, self.bg_pixmap)

        # Call the base class paintEvent
        super().paintEvent(event)
