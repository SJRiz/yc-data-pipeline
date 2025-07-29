import pandas as pd
from libs.db.db import engine

def load_to_postgres():
    df = pd.read_csv("data/processed/yc_clean.csv")
    df.to_sql("startups", engine, if_exists="append", index=False)

if __name__ == "__main__":
    load_to_postgres()