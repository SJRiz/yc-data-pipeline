import pandas as pd
from sqlalchemy import create_engine, MetaData, Table
from libs.app_config.config import DATABASE_URL

def load_to_postgres():
    # 1) Read your clean CSV into a DataFrame
    df = pd.read_csv("data/processed/yc_clean.csv")
    records = df.to_dict(orient="records")

    # 2) Spin up a brand‐new engine (guaranteed correct dialect)
    engine = create_engine(DATABASE_URL)

    # 3) Reflect the existing “startups” table
    metadata = MetaData()
    startups = Table("startups", metadata, autoload_with=engine)

    # 4) Use SQLAlchemy Core’s insert + executemany under the hood
    with engine.begin() as conn:
        conn.execute(startups.insert(), records)

if __name__ == "__main__":
    load_to_postgres()