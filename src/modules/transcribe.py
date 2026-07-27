from faster_whisper import WhisperModel
from google.cloud import speech


def transcribe_file(speech_file: str) -> str:
    """指定された音声ファイルを文字起こしする。"""
    client = speech.SpeechClient()

    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="ja-JP",
    )

    response = client.recognize(config=config, audio=audio)

    output = ""
    for result in response.results:
        output += result.alternatives[0].transcript

    return output


class LocalWhisperTranscriber:
    """ローカルでWhisperモデルを使用して音声ファイルを文字起こしするクラス。"""

    def __init__(self, model_size: str = "base"):
        # Initialize faster-whisper model
        # compute_type="int8" provides best CPU performance
        self.model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8"
        )

    def transcribe(self, audio_file: str) -> str:
        """指定された音声ファイルをWhisperモデルで文字起こしする。"""
        # faster-whisper returns (segments_generator, info) instead of dict
        segments, info = self.model.transcribe(
            audio_file,
            language="ja",
            beam_size=5,
            vad_filter=True  # Voice activity detection for better accuracy
        )

        # Combine all segments into single text
        transcript = "".join([segment.text for segment in segments])

        return transcript
