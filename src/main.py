import sys
import threading
import qtawesome as qta
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
                             QHBoxLayout, QComboBox, QLabel, QLineEdit, QScrollArea, QFrame, QSpacerItem, QSizePolicy, QScrollBar)
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QColor, QFont, QPixmap, QCursor
from modules.transcribe import transcribe_file
from modules.chat import get_gpt_completion
from modules.synthesize import synthesize_speech
from modules.playback import playback
from modules.record import record_audio
from src.gui.clickable_label import ClickableLabel


class VoiceInteractionThread(QThread):
    update_chat = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.running_event = threading.Event()
        self.recording_event = threading.Event()
        self.running_event.clear()
        self.recording_event.clear()
        self.voice_name = "ja-JP-Standard-A"  # Default voice name

    def run(self):
        while self.running_event.is_set():
            wav_path = record_audio(self.running_event, self.recording_event)
            if not self.running_event.is_set():
                break
            transcript = transcribe_file(wav_path)
            self.update_chat.emit("You", transcript)
            completion = get_gpt_completion(transcript)
            self.update_chat.emit("GPT", completion)
            synthesize_speech(completion, "output.wav", self.voice_name)
            playback("output.wav")

    def start_interaction(self):
        self.running_event.set()
        self.recording_event.set()
        self.start()

    def stop_interaction(self):
        self.running_event.clear()
        self.recording_event.clear()

    def stop_recording(self):
        self.recording_event.clear()

    def start_recording(self):
        self.recording_event.set()

    def set_voice(self, voice_name):
        self.voice_name = voice_name

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.voice_thread = VoiceInteractionThread()
        self.voice_thread.update_chat.connect(self.update_chat)
        self.gpt_name = "GPT"  # Default GPT name

    def initUI(self):
        self.setWindowTitle("Voice Interaction System")
        self.resize(800, 600)  # Set the window size to 800x600
        font = QFont()
        font.setFamily("メイリオ")

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        self.chat_widget = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_widget)
        self.chat_layout.addStretch(1)
        
        self.scroll_area.setWidget(self.chat_widget)

        self.mic_icon = qta.icon('fa5s.microphone')
        self.mic_button = QPushButton(self.mic_icon, "")

        self.mic_button.setStyleSheet('QPushButton {background-color: #C0C0C0; \
                                        height: 70px; \
                                        border: 3px solid black;\
                                        border-radius: 30px;} \
                                        QPushButton:pressed {background: #808080}')
        
        animation = qta.Spin(self.mic_button)
        self.spin_icon = qta.icon('fa5s.spinner', color='red', animation=animation)
        self.mic_button.setCheckable(True)
        self.mic_button.clicked.connect(self.toggle_interaction)

        stop_icon = qta.icon('fa5s.microphone-slash')
        self.stop_recording_button = QPushButton(stop_icon, "")
        self.stop_recording_button.setStyleSheet('QPushButton {background-color: #C0C0C0; \
                                                  height: 50px; \
                                                  border: 3px solid red;\
                                                  border-radius: 25px;} \
                                                  QPushButton:pressed {background: #808080}')
        self.stop_recording_button.clicked.connect(self.stop_recording)
        self.stop_recording_button.setEnabled(False)

        self.voice_selection = QComboBox()
        self.voice_selection.addItems(["ja-JP-Standard-A", "ja-JP-Standard-B", "ja-JP-Standard-C", "ja-JP-Standard-D"])
        self.voice_selection.setFont(font)
        self.voice_selection.setStyleSheet('QComboBox {background-color: #C0C0C0; \
                                                  height: 20px; \
                                                  border: 1px solid black;\
                                                  border-radius: 5px;} ')
        self.voice_selection.currentTextChanged.connect(self.update_voice_selection)

        self.gpt_name_input = QLineEdit()
        self.gpt_name_input.setPlaceholderText("Enter GPT Name")
        self.gpt_name_input.setFont(font)
        self.gpt_name_input.setStyleSheet('QLineEdit {background-color: #C0C0C0; \
                                                  height: 20px; \
                                                  border: 1px solid black;\
                                                  border-radius: 5px;} ')
        self.gpt_name_input.textChanged.connect(self.update_gpt_name)

        # Add Keyboard Input
        keyboard_icon = qta.icon('fa5s.keyboard')
        self.keyboard_button = QPushButton(keyboard_icon, "")

        self.keyboard_button.setStyleSheet('QPushButton {background-color: #C0C0C0; \
                                                  height: 50px; \
                                                  border: 3px solid black;\
                                                  border-radius: 25px;} \
                                                  QPushButton:pressed {background: #808080}')
        self.keyboard_button.clicked.connect(self.toggle_keyboard_input)

        self.keyboard_input = QLineEdit()
        self.keyboard_input.setPlaceholderText("Type your message here...")
        self.keyboard_input.setFont(font)
        self.keyboard_input.returnPressed.connect(self.send_keyboard_input)
        self.keyboard_input.setVisible(False)

        layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.keyboard_button)
        button_layout.addWidget(self.mic_button)
        button_layout.addWidget(self.stop_recording_button)

        layout.addWidget(self.scroll_area)
        layout.addWidget(self.voice_selection)
        layout.addWidget(self.gpt_name_input)
        layout.addWidget(self.keyboard_input)
        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def toggle_interaction(self, checked):
        if checked:
            self.mic_button.setIcon(self.spin_icon)
            self.voice_thread.start_interaction()
            self.stop_recording_button.setEnabled(True)
            self.keyboard_button.setEnabled(False)
            self.keyboard_input.setVisible(False)
        else:
            self.mic_button.setIcon(self.mic_icon)
            self.voice_thread.stop_interaction()
            self.stop_recording_button.setEnabled(False)
            self.keyboard_button.setEnabled(True)
    
    def toggle_keyboard_input(self):
        if self.keyboard_input.isVisible():
            self.keyboard_input.setVisible(False)
        else:
            self.keyboard_input.setVisible(True)
            self.keyboard_input.setFocus()

    def send_keyboard_input(self):
        text = self.keyboard_input.text()
        if text.strip():
            self.update_chat("You", text)
            completion = get_gpt_completion(text)
            self.update_chat("GPT", completion)
            self.keyboard_input.clear()

    def update_chat(self, sender, message):
        display_name = sender if sender != "GPT" else self.gpt_name
        self.append_chat_message(display_name, message)
        self.voice_thread.start_recording()
        self.stop_recording_button.setEnabled(True)

    def stop_recording(self):
        self.voice_thread.stop_recording()
        self.stop_recording_button.setEnabled(False)

    def update_voice_selection(self, voice_name):
        self.voice_thread.set_voice(voice_name)

    def update_gpt_name(self, name):
        self.gpt_name = name

    def append_chat_message(self, sender, message):
        bubble = self.create_bubble(sender, message)
        self.chat_layout.insertLayout(self.chat_layout.count() - 1, bubble)
        self.chat_widget.adjustSize()

        QTimer.singleShot(100, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def create_bubble(self, sender, message):
        bubble = QFrame()
        bubble_container = QHBoxLayout()
        bubble_layout = QVBoxLayout(bubble)
        
        bubble_label = QLabel(message)
        bubble_label.setWordWrap(True)

        bubble_label.setFont(QFont("メイリオ", 12))
        bubble_label.setStyleSheet("color: black; background-color: {}; border-radius: 15px; padding: 10px;".format('#E0F7FA' if sender == 'You' else '#E1FFC7'))
    
        sender_label = QLabel(sender)
        sender_label.setFont(QFont("メイリオ", 10, QFont.Bold))
        sender_label.setStyleSheet("color: gray;")  # 名前の色

        bubble_layout.addWidget(sender_label)
        bubble_layout.addWidget(bubble_label)
        bubble_layout.addStretch(1)

        sender_icon = ClickableLabel()

        if sender == "You":
            bubble.setStyleSheet("margin: 0px 0px 0px 100px;")
            sender_pixmap = QPixmap("../images/student-icon.png")
            bubble_container.addWidget(bubble)
            bubble_container.addWidget(sender_icon, alignment=Qt.AlignVCenter)
        else:
            bubble.setStyleSheet("margin: 0px 100px 0px 0px;")
            sender_pixmap = QPixmap("../images/chatgpt-icon.png")
            bubble_container.addWidget(sender_icon, alignment=Qt.AlignVCenter)
            bubble_container.addWidget(bubble)

        resized_sender_pixmap = sender_pixmap.scaledToHeight(50)
        sender_icon.setPixmap(resized_sender_pixmap)
        icon_size = resized_sender_pixmap.size()
        sender_icon.setFixedSize(icon_size.width(), icon_size.height())

        # make icon clickable
        sender_icon.setCursor(QCursor(Qt.PointingHandCursor))
        sender_icon.clicked.connect(self.on_icon_clicked)

        return bubble_container

    def on_icon_clicked(self):
        print("icon was clicked")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
