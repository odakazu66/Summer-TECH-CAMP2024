from modules.transcribe import transcribe_file
from modules.chat import get_gpt_completion
from modules.synthesize import synthesize_speech
from modules.playback import playback
from modules.record import record_audio

if __name__ == "__main__":
    wav_path = record_audio()
    transcript = transcribe_file(wav_path)
    completion = get_gpt_completion(transcript)
    synthesize_speech(completion, "output.wav")
    playback("output.wav")
