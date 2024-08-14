import pyaudio
import wave
import time
import numpy as np
from datetime import datetime

# 音声録音パラメータ
FORMAT = pyaudio.paInt16  # 16ビットの音声フォーマット
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
    audio = pyaudio.PyAudio()

    # ストリームを開く
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("録音を開始します...")

    frames = []
    silent_chunks = 0
    recording_started = False

    while running_event.is_set() and recording_event.is_set():
        data = stream.read(CHUNK)
        data_int = np.frombuffer(data, dtype=np.int16)

        if not recording_started:
            if not is_silent(data_int):
                print("音声を検出しました。録音を開始します...")
                recording_started = True
                frames.append(data)
        else:
            frames.append(data)
            if is_silent(data_int):
                silent_chunks += 1
            else:
                silent_chunks = 0

            if silent_chunks > SILENCE_DURATION * RATE / CHUNK:
                print("無音が続いたため、録音を終了します...")
                break

    if not running_event.is_set():
        print("会話が停止されました")
        return None


    # ストリームを閉じる
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # 録音したデータをwavファイルとして保存
    now = datetime.now()
    output_filename = now.strftime("../sound/user_%Y_%m_%d_%H_%M_%S.wav")

    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"録音が完了しました。{output_filename}に保存されました。")
    return output_filename

if __name__ == "__main__":
    file_path = record_audio()
