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
        # Try multiple compute types for better compatibility
        import platform

        compute_types = ["int8", "float32"]

        # On Windows, prefer float32 for better compatibility
        if platform.system() == "Windows":
            compute_types = ["float32", "int8"]

        last_error = None
        for compute_type in compute_types:
            try:
                print(f"Trying to load Whisper model with compute_type={compute_type}...")
                self.model = WhisperModel(
                    model_size,
                    device="cpu",
                    compute_type=compute_type
                )
                print(f"Successfully loaded Whisper model with compute_type={compute_type}")
                return
            except Exception as e:
                last_error = e
                print(f"Failed to load with compute_type={compute_type}: {e}")
                continue

        # If we get here, all compute types failed
        raise RuntimeError(
            f"Failed to initialize Whisper model with any compute type. "
            f"Last error: {last_error}. "
            f"Please ensure all dependencies are properly installed."
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
