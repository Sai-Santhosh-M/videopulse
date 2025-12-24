import whisper
import os
import sys

ffmpeg_path = r"C:\ffmpeg\bin"
os.environ["PATH"] += os.pathsep + ffmpeg_path

def transcribe_audio(audio_file="audio.mp3", output_file="transcript.txt"):
    print("[...] Loading Whisper model...")
    model = whisper.load_model("base")  # or "small", "medium", "large"

    print("[...] Transcribing audio...")
    result = model.transcribe(audio_file)

    text = result['text']
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[✓] Transcript saved to {output_file}")

if __name__ == "__main__":
    audio_file = "audio.mp3"
    print("Current working directory:", os.getcwd())

    if not os.path.exists(audio_file):
        print(f"[X] {audio_file} not found. Please run get_audio.py first.")
        sys.exit(1)

    try:
        transcribe_audio(audio_file)
    except Exception as e:
        print("[X] Failed to transcribe:", str(e))
