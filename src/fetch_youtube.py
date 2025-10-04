from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Get the API key
api_key = os.getenv("YOUTUBE_API_KEY")

# Test
if api_key:
    print("✅ API key loaded successfully:", api_key[:10] + "...")
else:
    print("❌ Could not load API key. Check your .env file.")

from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
import json

# Load API key
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

# Build YouTube API client
youtube = build("youtube", "v3", developerKey=API_KEY)

# Replace with your channel ID
CHANNEL_ID = "UCUFoQUaVRt3MVFxqwPUMLCQ"

# Fetch channel info
channel_response = youtube.channels().list(
    part="snippet,contentDetails,statistics",
    id=CHANNEL_ID
).execute()

# Print pretty JSON output
print(json.dumps(channel_response, indent=2))

# Get the uploads playlist ID
def get_uploads_playlist(channel_response):
    return channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

uploads_playlist_id = get_uploads_playlist(channel_response)
print("Uploads playlist ID:", uploads_playlist_id)

def get_all_video_ids(playlist_id):
    video_ids = []
    next_page_token = None
    while True:
        resp = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,          # max allowed per request
            pageToken=next_page_token
        ).execute()

        for item in resp.get("items", []):
            video_ids.append(item["contentDetails"]["videoId"])

        next_page_token = resp.get("nextPageToken")
        if not next_page_token:
            break

    return video_ids

video_ids = get_all_video_ids(uploads_playlist_id)
print(f"Found {len(video_ids)} videos")

def chunker(seq, size):
    # Helper to split list into chunks
    for i in range(0, len(seq), size):
        yield seq[i:i+size]

def fetch_videos_stats(video_ids):
    all_videos = []
    for chunk in chunker(video_ids, 50):  # API allows up to 50 IDs per call
        resp = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=",".join(chunk)
        ).execute()
        all_videos.extend(resp.get("items", []))
    return all_videos

videos_data = fetch_videos_stats(video_ids)
print(f"Fetched stats for {len(videos_data)} videos")

import json
import os

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

with open(os.path.join(RAW_DIR, f"videos_{CHANNEL_ID}.json"), "w", encoding="utf-8") as f:
    json.dump(videos_data, f, indent=2)

print("Saved video data to raw folder")

