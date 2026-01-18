import miniaudio
from PyQt5.QtCore import QThread, pyqtSignal
import time


# use this function when the parent is already running in a thread
def playback(filename):
    """Blocking playback using miniaudio"""
    # Decode file to get audio properties
    decoded = miniaudio.decode_file(filename)

    # Create playback device
    device = miniaudio.PlaybackDevice(
        output_format=decoded.sample_format,
        nchannels=decoded.nchannels,
        sample_rate=decoded.sample_rate
    )

    # Use stream_file for convenient streaming
    stream = miniaudio.stream_file(
        filename,
        output_format=decoded.sample_format,
        nchannels=decoded.nchannels,
        sample_rate=decoded.sample_rate
    )

    # Start playback
    device.start(stream)

    # Wait for playback to complete
    total_frames = len(decoded.samples) // decoded.nchannels
    duration = total_frames / decoded.sample_rate
    time.sleep(duration + 0.2)

    device.close()


# use this class when we need a non-blocking way to play sound
class PlaybackThread(QThread):
    playback_finished = pyqtSignal()

    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.is_stopped = False
        self.device = None

    def run(self):
        """Non-blocking playback with stop capability"""
        try:
            # Decode file to get audio properties
            decoded = miniaudio.decode_file(self.filename)

            # Create playback device
            self.device = miniaudio.PlaybackDevice(
                output_format=decoded.sample_format,
                nchannels=decoded.nchannels,
                sample_rate=decoded.sample_rate
            )

            # Use stream_file for convenient streaming
            stream = miniaudio.stream_file(
                self.filename,
                output_format=decoded.sample_format,
                nchannels=decoded.nchannels,
                sample_rate=decoded.sample_rate
            )

            # Start playback
            self.device.start(stream)

            # Wait for playback to complete or stop
            total_frames = len(decoded.samples) // decoded.nchannels
            duration = total_frames / decoded.sample_rate
            elapsed = 0

            while elapsed < duration and not self.is_stopped:
                time.sleep(0.05)
                elapsed += 0.05

            self.device.close()

        except Exception as e:
            print(f"Playback error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.playback_finished.emit()

    def stop_playback(self):
        """Stop playback immediately"""
        self.is_stopped = True
        if self.device:
            try:
                self.device.stop()
                self.device.close()
            except:
                pass
