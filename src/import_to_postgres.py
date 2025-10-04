import pandas as pd
from sqlalchemy import create_engine

# CSV file path
csv_file = r"C:\Users\Visheshaditya\Desktop\youtube-analytics\data\videos_UCUFoQUaVRt3MVFxqwPUMLCQ.csv"


# PostgreSQL connection
user = "postgres"
password = "vio"
host = "localhost"
port = "5432"
database = "youtube_analytics"

engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")

# Load CSV into pandas
df = pd.read_csv(csv_file)

# Write to PostgreSQL
df.to_sql("videos", engine, if_exists="replace", index=False)
print("✅ CSV imported successfully!")
