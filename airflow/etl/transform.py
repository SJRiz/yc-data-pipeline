import json, pandas as pd, os

def transform_yc_data():
    raw = json.load(open("data/raw/yc_raw.json"))
    df = pd.DataFrame(raw)
    
    df['tags'] = df['tags'].apply(lambda L: [t.lower() for t in L])
    df.drop_duplicates('name', inplace=True)
    os.makedirs("data/processed", exist_ok=True)  # Ensure directory exists
    df.to_csv("data/processed/yc_clean.csv", index=False)

if __name__ == "__main__":
    transform_yc_data()