# synthesize.py
from google.cloud import texttospeech
from gtts import gTTS
import librosa
import soundfile as sf
import os


def synthesize_speech(text: str, output_file: str, voice_name: str):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        name=voice_name,
        language_code="ja-JP",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print(f'オーディオコンテンツがファイル "{output_file}" に書き込まれました')


def gtts_synthesize_speech(text: str, output_file: str, lang: str = "ja"):
    # Save as MP3 first
    temp_mp3 = output_file.replace(".wav", ".mp3")
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(temp_mp3)

    # Convert to WAV
    y, sr = librosa.load(temp_mp3, sr=None)
    sf.write(output_file, y, sr)

    # Clean up temporary MP3
    os.remove(temp_mp3)

    print(f'オーディオコンテンツがファイル "{output_file}" に書き込まれました')
