import sys
import argparse
import threading
from datetime import datetime
import qtawesome as qta
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
                             QHBoxLayout, QComboBox, QLabel, QLineEdit, QScrollArea, QFrame, QSpacerItem, QSizePolicy, QScrollBar)
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QColor, QFont, QPixmap, QCursor
from modules.transcribe import transcribe_file
from modules.chat import get_gpt_completion, load_conversation, file_path
from modules.chat import main as chat_main
from modules.synthesize import synthesize_speech
from modules.playback import playback
from modules.record import record_audio
from gui.clickable_label import ClickableLabel
from gui.user_profile_dialog import UserProfileDialog
from gui.gpt_profile_dialog import GPTProfileDialog
from gui.chat_bubble import ChatBubble


class VoiceInteractionThread(QThread):
    update_chat = pyqtSignal(dict)

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
            self.update_chat.emit({
                'sender_id': "You",
                "transcript": transcript,
                "sound_path": wav_path
            })

            now = datetime.now()
            output_filename = now.strftime("../sound/gpt_%Y_%m_%d_%H_%M_%S.wav")

            completion = get_gpt_completion(transcript, user_sound_path=wav_path, gpt_sound_path=output_filename)

            synthesize_speech(completion, output_filename, self.voice_name)

            self.update_chat.emit({
                'sender_id': "GPT",
                "transcript": completion,
                "sound_path": output_filename
            })

            playback(output_filename)

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
        self.voice_thread = VoiceInteractionThread()
        self.voice_thread.update_chat.connect(self.update_chat)
        self.gpt_name = "GPT"  # Default GPT name
        self.user_name = "You"
        self.user_icon_path = "../images/student-icon.png"
        self.gpt_icon_path = "../images/chatgpt-icon.png"
        self.chat_bubbles_list = []

        self.initUI()

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

        # Load Conversation History
        self.load_conversation_gui()

    def load_conversation_gui(self):
        messages = load_conversation(file_path)["messages"]

        if (len(messages) - 1) == 0: # subtract 1 because of system prompt
            print("There is no history, using only system prompt")
            return

        for message in messages:
            if message["role"] == "user":
                self.append_chat_message("You", message["content"])
            elif message["role"] == "assistant":
                self.append_chat_message("GPT", message["content"])

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
            #self.update_chat("You", text)
            self.update_chat({
                "sender_id": "You",
                "transcript": text
            })
            completion = get_gpt_completion(text)
            #self.update_chat("GPT", completion)
            self.update_chat({
                "sender_id": "GPT",
                "transcript": completion
            })
            self.keyboard_input.clear()

    def update_chat(self, data):
        sender_id = data.get('sender_id')
        message = data.get('transcript')
        sound_path = data.get('sound_path')

        self.append_chat_message(sender_id, message, sound_path=sound_path)
        self.voice_thread.start_recording()
        self.stop_recording_button.setEnabled(True)

    def stop_recording(self):
        self.voice_thread.stop_recording()
        self.stop_recording_button.setEnabled(False)

    def update_voice_selection(self, voice_name):
        self.voice_thread.set_voice(voice_name)

    def update_gpt_name(self, name):
        self.gpt_name = name

    def append_chat_message(self, sender_id, message, sound_path=None):
        bubble = self.create_bubble(sender_id, message, sound_path=sound_path)
        self.chat_layout.insertLayout(self.chat_layout.count() - 1, bubble)
        self.chat_widget.adjustSize()

        QTimer.singleShot(100, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def create_bubble(self, sender_id, message, sound_path=None):
        return ChatBubble(sender_id, message, self, sound_path=sound_path)

    def update_chat_names(self, dialog_id, old_name, new_name):
        if dialog_id == "You":
            self.set_user_name(new_name)
        else:
            self.set_gpt_name(new_name)

        # Loop through all items in the chat layout
        for i in range(self.chat_layout.count() - 1):  # Exclude the last item (stretch)
            # Get the layout containing the bubble container (QHBoxLayout)
            bubble_container = self.chat_layout.itemAt(i).layout()

            if bubble_container is not None:
                # Loop through the items in the bubble container to find the QFrame (chat bubble)
                for j in range(bubble_container.count()):
                    item = bubble_container.itemAt(j).widget()
                    if isinstance(item, QFrame):  # Ensure the item is a QFrame (chat bubble)
                        bubble = item

                        # Get the QVBoxLayout inside the QFrame
                        bubble_layout = bubble.layout()

                        if bubble_layout is not None:
                            # The first item in the QVBoxLayout is the sender label
                            sender_label = bubble_layout.itemAt(0).widget()
                            if isinstance(sender_label, QLabel):
                                if sender_label.text() == old_name:
                                    # Update the sender name
                                    sender_label.setText(new_name)

    def update_user_icons(self, user, icon_path):
        if user == "You":
            self.set_user_icon_path(icon_path)
        else:
            self.set_gpt_icon_path(icon_path)

        # Loop through all items in the chat layout
        for i in range(self.chat_layout.count() - 1):  # Exclude the last item (stretch)
            # Get the layout containing the bubble container (QHBoxLayout)
            bubble_container = self.chat_layout.itemAt(i).layout()

            if bubble_container is not None:
                # Loop through the items in the bubble container to find the QFrame (chat bubble)
                for j in range(bubble_container.count()):
                    item = bubble_container.itemAt(j).widget()
                    # to check order or qtItems
                    # print(type(item))
                    if isinstance(item, ClickableLabel):
                        if item.id == "You":
                            item.set_icon(self.user_icon_path)
                        else:
                            item.set_icon(self.gpt_icon_path)

    def set_gpt_icon_path(self, new_icon_path):
        self.gpt_icon_path = new_icon_path

    def set_user_icon_path(self, new_icon_path):
        self.user_icon_path = new_icon_path

    def set_gpt_name(self, name):
        self.gpt_name = name

    def set_user_name(self, name):
        self.user_name = name

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--use-gui", action="store_true", help="use the gui")

    args = parser.parse_args()

    if not args.use_gui:
        chat_main()
    else:
        app = QApplication(sys.argv)
        mainWindow = MainWindow()
        mainWindow.show()
        sys.exit(app.exec_())