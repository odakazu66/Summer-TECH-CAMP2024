class ChatBubble(QHBoxLayout):
    def __init__(self, sender, message, parent=None):
        super().__init__(parent)
        bubble = QFrame()


