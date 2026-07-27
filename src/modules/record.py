import miniaudio
import wave
import numpy as np
from datetime import datetime
import time
import threading

# 音声録音パラメータ
SAMPLE_FORMAT = miniaudio.SampleFormat.SIGNED16  # 16ビットの音声フォーマット
CHANNELS = 1  # モノラル
RATE = 44100  # サンプリングレート
CHUNK = 1024  # チャンクサイズ
THRESHOLD = 500  # 音声検出の閾値
SILENCE_DURATION = 2  # 無音と判定する秒数

def is_silent(data, threshold=THRESHOLD):
    """データが無音かどうかを判定"""
    return max(data) < threshold

def record_audio(running_event, recording_event):
    """音声を録音し、wavファイルとして保存する"""

    print("録音を開始します...")

    frames = []
    silent_chunks = 0
    recording_started = False
    should_stop = threading.Event()

    # Generator function to receive audio data
    def capture_callback():
        nonlocal recording_started, silent_chunks, frames
        try:
            while not should_stop.is_set():
                # Receive audio data from miniaudio
                audio_data = yield

                if audio_data is None:
                    continue

                if not running_event.is_set() or not recording_event.is_set():
                    should_stop.set()
                    break

                # Convert to numpy array
                data_int = np.frombuffer(audio_data, dtype=np.int16)

                if not recording_started:
                    if not is_silent(data_int):
                        print("音声を検出しました。録音を開始します...")
                        recording_started = True
                        frames.append(audio_data)
                else:
                    frames.append(audio_data)
                    if is_silent(data_int):
                        silent_chunks += 1
                    else:
                        silent_chunks = 0

                    if silent_chunks > SILENCE_DURATION * RATE / (RATE * 0.2):  # Adjust for buffer size
                        print("無音が続いたため、録音を終了します...")
                        should_stop.set()
                        break
        except GeneratorExit:
            pass

    # Create capture device
    device = miniaudio.CaptureDevice(
        input_format=SAMPLE_FORMAT,
        nchannels=CHANNELS,
        sample_rate=RATE,
        buffersize_msec=200  # 200ms buffer
    )

    # Start recording with callback generator
    generator = capture_callback()
    next(generator)  # Prime the generator

    try:
        device.start(generator)

        # Wait until recording is done
        while not should_stop.is_set() and running_event.is_set() and recording_event.is_set():
            time.sleep(0.01)

    finally:
        device.close()

    if not running_event.is_set():
        print("会話が停止されました")
        return None

    if not frames:
        print("音声が録音されませんでした")
        return None

    # 録音したデータをwavファイルとして保存
    now = datetime.now()
    output_filename = now.strftime("../sound/user_%Y_%m_%d_%H_%M_%S.wav")

    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # 16-bit = 2 bytes
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"録音が完了しました。{output_filename}に保存されました。")
    return output_filename

if __name__ == "__main__":
    running = threading.Event()
    recording = threading.Event()
    running.set()
    recording.set()
    file_path = record_audio(running, recording)
