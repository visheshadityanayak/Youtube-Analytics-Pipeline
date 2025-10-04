import os
import json
import pandas as pd

# Paths
RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "raw")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

CHANNEL_ID = "UCUFoQUaVRt3MVFxqwPUMLCQ"
RAW_FILE = os.path.join(RAW_DIR, f"videos_{CHANNEL_ID}.json")
CSV_FILE = os.path.join(DATA_DIR, f"videos_{CHANNEL_ID}.csv")

# Load raw JSON
with open(RAW_FILE, "r", encoding="utf-8") as f:
    videos_data = json.load(f)

# Extract relevant fields
video_list = []
for video in videos_data:
    snippet = video.get("snippet", {})
    stats = video.get("statistics", {})
    content = video.get("contentDetails", {})

    video_list.append({
        "video_id": video.get("id"),
        "title": snippet.get("title"),
        "published_at": snippet.get("publishedAt"),
        "description": snippet.get("description"),
        "view_count": int(stats.get("viewCount", 0)),
        "like_count": int(stats.get("likeCount", 0)),
        "comment_count": int(stats.get("commentCount", 0)),
        "duration": content.get("duration")
    })


# Create DataFrame
df = pd.DataFrame(video_list)

# Save to CSV
df.to_csv(CSV_FILE, index=False, encoding="utf-8")
print(f"✅ Saved CSV to {CSV_FILE}")

import os
import json
import pandas as pd
import isodate  # to convert ISO 8601 durations to minutes

# Paths
RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "raw")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

CHANNEL_ID = "UCUFoQUaVRt3MVFxqwPUMLCQ"
RAW_FILE = os.path.join(RAW_DIR, f"videos_{CHANNEL_ID}.json")
CSV_FILE = os.path.join(DATA_DIR, f"videos_{CHANNEL_ID}.csv")

# Load raw JSON
with open(RAW_FILE, "r", encoding="utf-8") as f:
    videos_data = json.load(f)

# Extract relevant fields
video_list = []
for video in videos_data:
    snippet = video.get("snippet", {})
    stats = video.get("statistics", {})
    content = video.get("contentDetails", {})

    # Convert duration to minutes
    iso_duration = content.get("duration", "PT0S")
    duration_minutes = isodate.parse_duration(iso_duration).total_seconds() / 60

    # Extract numeric stats safely
    view_count = int(stats.get("viewCount", 0))
    like_count = int(stats.get("likeCount", 0))
    comment_count = int(stats.get("commentCount", 0))

    video_list.append({
        "video_id": video.get("id"),
        "title": snippet.get("title"),
        "published_at": pd.to_datetime(snippet.get("publishedAt")),
        "description": snippet.get("description"),
        "view_count": view_count,
        "like_count": like_count,
        "comment_count": comment_count,
        "duration_minutes": duration_minutes,
        "likes_per_view": like_count / view_count if view_count > 0 else 0,
        "comments_per_view": comment_count / view_count if view_count > 0 else 0
    })

# Create DataFrame
df = pd.DataFrame(video_list)

# Save to CSV
df.to_csv(CSV_FILE, index=False, encoding="utf-8")
print(f"✅ Saved transformed CSV to {CSV_FILE}")


