import argparse
from modules.transcribe import transcribe_file
from modules.chat import get_completion
from modules.synthesize import synthesize_speech
from modules.record import record_audio

if __name__ == "__main__":
    wav_path = record_audio()
    transcript = transcribe_file(wav_path)
    completion = get_completion(transcript)
    synthesize_speech(completion, "output.wav")
