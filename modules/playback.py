import wave
import pyaudio

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