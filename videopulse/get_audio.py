import sys
import re
import os
from yt_dlp import YoutubeDL

FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"  

def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else None

def download_audio(url, output_path="audio"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'ffmpeg_location': FFMPEG_PATH,  
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,  
        'no_warnings': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print(f"[✓] Audio downloaded to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[!] Usage: python get_audio.py <YouTube URL>")
        sys.exit(1)

    url = sys.argv[1]
    video_id = extract_video_id(url)

    if not video_id:
        print("[X] Could not extract video ID from URL.")
        sys.exit(1)

    try:
        print(f"[...] Downloading audio using ffmpeg at: {FFMPEG_PATH}")
        download_audio(url)
    except Exception as e:
        print("[X] Failed to download audio:", str(e))
