import os
import re
import sys
import json
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key safely
API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    print("❌ YOUTUBE_API_KEY not found in environment variables")
    sys.exit(1)

# UTF-8 safe output (Windows fix)
try:
    sys.stdout.reconfigure(encoding="utf-8")
except:
    pass

def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else None

def fetch_comments(video_id, api_key, max_comments=None):
    youtube = build("youtube", "v3", developerKey=api_key)
    comments = []
    next_page_token = None
    fetched = 0

    print("[...] Starting comment fetch...")

    while True:
        try:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                pageToken=next_page_token,
                maxResults=100,
                textFormat="plainText"
            )
            response = request.execute()
        except Exception as e:
            print("[X] API error while fetching:", str(e))
            break

        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)
            fetched += 1

            if max_comments and fetched >= max_comments:
                print(f"[✓] Reached max limit of {max_comments} comments.")
                break

        next_page_token = response.get("nextPageToken")
        if not next_page_token or (max_comments and fetched >= max_comments):
            break

        print(f"[...] Fetched so far: {fetched} comments...")

    print(f"[✓] Total fetched: {len(comments)} comments.")
    with open("comments.json", "w", encoding="utf-8") as f:
        json.dump(comments, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[!] Usage: python youtube.py <YouTube URL>")
        sys.exit(1)

    url = sys.argv[1]
    video_id = extract_video_id(url)

    if not video_id:
        print("[X] Could not extract video ID from URL.")
        sys.exit(1)

    try:
        fetch_comments(video_id, API_KEY)  # To limit: add max_comments=5000
    except Exception as e:
        print("[X] Failed to fetch comments:", str(e))