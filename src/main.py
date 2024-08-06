# main.py
import sys
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget, QHBoxLayout, QComboBox
from PyQt5.QtCore import QThread, pyqtSignal
from modules.transcribe import transcribe_file
from modules.chat import get_gpt_completion
from modules.synthesize import synthesize_speech
from modules.playback import playback
from modules.record import record_audio

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

    def initUI(self):
        self.setWindowTitle("Voice Interaction System")

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)

        self.mic_button = QPushButton("Start Interaction")
        self.mic_button.setCheckable(True)
        self.mic_button.clicked.connect(self.toggle_interaction)

        self.stop_recording_button = QPushButton("Stop Speaking")
        self.stop_recording_button.clicked.connect(self.stop_recording)
        self.stop_recording_button.setEnabled(False)

        self.voice_selection = QComboBox()
        self.voice_selection.addItems(["ja-JP-Standard-A", "ja-JP-Standard-B", "ja-JP-Standard-C", "ja-JP-Standard-D"])
        self.voice_selection.currentTextChanged.connect(self.update_voice_selection)

        layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.mic_button)
        button_layout.addWidget(self.stop_recording_button)

        layout.addWidget(self.chat_display)
        layout.addWidget(self.voice_selection)
        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def toggle_interaction(self, checked):
        if checked:
            self.mic_button.setText("Stop Interaction")
            self.voice_thread.start_interaction()
            self.stop_recording_button.setEnabled(True)
        else:
            self.mic_button.setText("Start Interaction")
            self.voice_thread.stop_interaction()
            self.stop_recording_button.setEnabled(False)

    def update_chat(self, sender, message):
        self.chat_display.append(f"{sender}: {message}")
        self.voice_thread.start_recording()
        self.stop_recording_button.setEnabled(True)

    def stop_recording(self):
        self.voice_thread.stop_recording()
        self.stop_recording_button.setEnabled(False)

    def update_voice_selection(self, voice_name):
        self.voice_thread.set_voice(voice_name)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
