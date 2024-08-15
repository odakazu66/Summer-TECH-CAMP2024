import wave
import pyaudio
from PyQt5.QtCore import QThread, pyqtSignal


# use this class when the parent is already running in a thread
def playback(filename):
    CHUNK = 1024

    w = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(w.getsampwidth()),
                    channels=w.getnchannels(),
                    rate=w.getframerate(),
                    output=True)

    data = w.readframes(CHUNK)
    while len(data) > 0:
        stream.write(data)
        data = w.readframes(CHUNK)

    stream.stop_stream()
    stream.close()
    p.terminate()

# use this class when we need a non-blocking way to play sound
class PlaybackThread(QThread):
    playback_finished = pyqtSignal()

    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.is_stopped = False

    def run(self):
        CHUNK = 1024
        w = wave.open(self.filename, 'rb')
        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(w.getsampwidth()),
                        channels=w.getnchannels(),
                        rate=w.getframerate(),
                        output=True)

        data = w.readframes(CHUNK)
        while len(data) > 0 and not self.is_stopped:
            stream.write(data)
            data = w.readframes(CHUNK)

        stream.stop_stream()
        stream.close()
        p.terminate()

        self.playback_finished.emit()

    def stop_playback(self):
        self.is_stopped = True
