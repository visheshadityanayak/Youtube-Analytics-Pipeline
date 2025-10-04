import pandas as pd
import os

# Path to your CSV
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
CHANNEL_ID = "UCUFoQUaVRt3MVFxqwPUMLCQ"
CSV_FILE = os.path.join(DATA_DIR, f"videos_{CHANNEL_ID}.csv")

# Load CSV
df = pd.read_csv(CSV_FILE)

# Quick checks
print("Columns:", df.columns.tolist())
print("Total videos:", len(df))
print("First 5 rows:")
print(df.head())

# Optional: check stats for new columns
print("\nSample duration_minutes:")
print(df["duration_minutes"].head())
print("\nSample likes_per_view:")
print(df["likes_per_view"].head())
print("\nSample comments_per_view:")
print(df["comments_per_view"].head())

