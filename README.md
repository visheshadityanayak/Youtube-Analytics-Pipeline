# YouTube Analytics Dashboard & Data Pipeline

## Project Overview
This project fetches YouTube channel data using the YouTube API, stores it in a PostgreSQL database, and provides an interactive **Streamlit dashboard** for analytics.  
It demonstrates skills in **data engineering, ETL pipelines, database management, and dashboard visualization**.

---

## Features
- Fetches **video metadata** (views, likes, comments, duration) from any channel using its ID.  
- Stores data in a **PostgreSQL database**.  
- Provides an **interactive Streamlit dashboard** with:
  - KPIs: Total videos, views, likes, comments, average duration  
  - Trends: Views and likes over time  
  - Scatter plots: Views vs Likes  
  - Video performance table  
- Supports **date filtering** and dynamic visualizations.  
- Configurable to analyze **different channels** by changing channel ID.  

---

## Live Demo
[Insert your deployed Streamlit app link here]

---

## Project Structure
youtube-analytics/
│
├─ app.py # Streamlit dashboard
├─ src/ # Pipeline scripts
│ ├─ fetch_youtube.py
│ ├─ import_to_postgres.py
│ └─ transform_youtube.py
├─ data/videos.csv # Processed CSV data
├─ raw/videos.json # Raw JSON data from API
├─ requirements.txt # Python dependencies
├─ .gitignore # Ignored files (venv, .env, cache)
├─ .env # Local environment variables (ignored)
├─ .env.example # Example environment variables
├─ .idea/ # IDE settings (optional)
└─ .venv/ # Virtual environment (ignored)


---

## Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/youtube-analytics.git
cd youtube-analytics


2. Install dependencies : pip install -r requirements.txt


3. Configure environment variables

Copy .env.example to .env and fill in your credentials:

POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=youtube_db
YOUTUBE_API_KEY=your_api_key

4. Set up PostgreSQL database

Create a database matching your .env settings.

Run the pipeline scripts in src/ to fetch and store data:

python src/fetch_youtube.py
python src/import_to_postgres.py
python src/transform_youtube.py

5. Run the Streamlit dashboard
streamlit run app.py



Usage
Change CHANNEL_ID in src/fetch_youtube.py to fetch data for different channels.
Use the dashboard sidebar filters to analyze data for specific date ranges.



Technologies Used

Python, Pandas, SQLAlchemy, PostgreSQL
Streamlit & Plotly for interactive dashboards
YouTube Data API v3


Future Improvements

Automate the pipeline with Airflow or cron jobs.
Include subscriber and revenue analytics.
Support multiple channels in the dashboard.


