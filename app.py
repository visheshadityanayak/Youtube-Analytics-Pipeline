import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# ---- Database connection ----
DB_USER = "postgres"            # your Postgres username
DB_PASSWORD = "vio"   # your Postgres password
DB_HOST = "Localhost"
DB_PORT = "5432"
DB_NAME = "youtube_analytics"          # your database name

# create SQLAlchemy engine
engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")


@st.cache_data
def load_data():
    query = "SELECT * FROM videos;"
    df = pd.read_sql(query, engine)

    # Convert published_at to datetime
    df['published_at'] = pd.to_datetime(df['published_at'])
    return df


df = load_data()


#streamlit layout
channel_name = "StudioBinder"
channel_pfp_url = "https://yt3.googleusercontent.com/ytc/AIdro_l-Xw29jFGgFUudxkKn2F7S51-JCDRiC8TWzLHJf5RXt34=s160-c-k-c0x00ffffff-no-rj"

st.markdown(
    f"### <img src='{channel_pfp_url}' width='50' style='vertical-align:middle'> {channel_name}'s YouTube Channel Analytics Dashboard",
    unsafe_allow_html=True
)


st.subheader("Sample Data")
st.dataframe(df.head())

#date filter
st.subheader("Filter by Date")
start_date = st.date_input("Start Date", df['published_at'].min())
end_date = st.date_input("End Date", df['published_at'].max())

# Filter the dataframe
# Ensure both sides are timezone-naive
df['published_at'] = pd.to_datetime(df['published_at']).dt.tz_localize(None)

filtered_df = df[
    (df['published_at'] >= pd.to_datetime(start_date)) &
    (df['published_at'] <= pd.to_datetime(end_date))
]


st.write(f"Showing {len(filtered_df)} videos")


#top n videos by views
st.subheader("Top Videos by Views")
top_n = st.slider("Select Top N videos", min_value=5, max_value=20, value=10)
top_videos = filtered_df.sort_values(by="view_count", ascending=False).head(top_n)
st.bar_chart(top_videos.set_index("title")["view_count"])

#engagement metrics scatter plot
st.subheader("Likes vs Views")
st.scatter_chart(filtered_df[['view_count', 'like_count']])


#engagement overtime
st.subheader("Comments per View Over Time")
time_series = filtered_df.groupby(filtered_df['published_at'].dt.to_period('M')).agg({
    'view_count': 'sum',
    'like_count': 'sum',
    'comment_count': 'sum'
}).reset_index()

time_series['published_at'] = time_series['published_at'].astype(str)
st.line_chart(time_series.set_index('published_at')[['view_count', 'like_count', 'comment_count']])

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# Database connection
engine = create_engine("postgresql+psycopg2://postgres:vio@localhost:5432/youtube_analytics")

st.set_page_config(page_title="YouTube Analytics Dashboard", layout="wide")
st.title("📊 YouTube Analytics Dashboard")

# Load data
@st.cache_data
def load_data():
    query = "SELECT * FROM videos;"
    df = pd.read_sql(query, engine)
    df['published_at'] = pd.to_datetime(df['published_at'])
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
start_date = st.sidebar.date_input("Start Date", df['published_at'].min().date())
end_date = st.sidebar.date_input("End Date", df['published_at'].max().date())

filtered_df = df[(df['published_at'] >= pd.to_datetime(start_date)) &
                 (df['published_at'] <= pd.to_datetime(end_date) + pd.Timedelta(days=1))]


# KPIs
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Videos", len(filtered_df))
col2.metric("Total Views", f"{filtered_df['view_count'].sum():,}")
col3.metric("Total Likes", f"{filtered_df['like_count'].sum():,}")
col4.metric("Total Comments", f"{filtered_df['comment_count'].sum():,}")
col5.metric("Avg Duration (min)", round(filtered_df['duration_minutes'].mean(), 2))

st.markdown("---")

# Charts
tab1, tab2, tab3 = st.tabs(["📈 Trends", "📊 Distributions", "📋 Video Table"])

with tab1:
    st.subheader("Views and Likes Over Time")
    trend_df = filtered_df.groupby('published_at')[['view_count', 'like_count']].sum().reset_index()
    fig1 = px.line(trend_df, x='published_at', y=['view_count', 'like_count'],
                   labels={'value': 'Count', 'published_at': 'Date'},
                   title="Views and Likes Trend")
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    st.subheader("Views vs Likes Scatter Plot")
    fig2 = px.scatter(filtered_df, x='view_count', y='like_count',
                      hover_data=['title'], size='duration_minutes',
                      title="Engagement Correlation: Views vs Likes")
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("Video Performance Table")
    st.dataframe(filtered_df[['title', 'view_count', 'like_count', 'comment_count', 'duration_minutes']].sort_values(by='view_count', ascending=False))


st.set_page_config(page_title="YouTube Analytics Dashboard", layout="wide")




st.markdown("✅ Data source: PostgreSQL | Visualized with Streamlit + Plotly")










