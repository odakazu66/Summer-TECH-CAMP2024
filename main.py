import argparse
from modules.transcribe import transcribe_file
from modules.chat import get_completion
from modules.synthesize import synthesize_speech

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="音声ファイルを文字起こしして翻訳し、音声に合成するスクリプト")
    parser.add_argument("path", help="文字起こしする音声ファイルのファイルパスまたは GCS パス")
    args = parser.parse_args()

    transcript = transcribe_file(args.path)
    completion = get_completion(transcript)
    synthesize_speech(completion, "output.wav")
