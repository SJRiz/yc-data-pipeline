import ast
import pandas as pd
from sqlalchemy import MetaData, Table
from libs.db.db import engine

def load_to_postgres():
    df = pd.read_csv("./data/processed/yc_clean.csv")
    df['tags'] = df['tags'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
    df['industries'] = df['industries'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
    records = df.to_dict(orient="records")

    # Reflect the existing “startups” table
    metadata = MetaData()
    startups = Table("startups", metadata, autoload_with=engine)

    with engine.begin() as conn:
        conn.execute(startups.insert(), records)

if __name__ == "__main__":
    load_to_postgres()