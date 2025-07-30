import json, csv
import pandas as pd
import os

def transform_yc_data():

    with open("./data/raw/yc_raw.json", "r", encoding="utf-8") as f:
        raw = json.load(f)

    df = pd.DataFrame(raw)

    # --- Safely lower-case list items ---
    def clean_list(L):
        if isinstance(L, list):
            return [str(t).lower() for t in L if isinstance(t, str)]
        return []

    df['tags'] = df['tags'].apply(clean_list)
    df['industries'] = df['industries'].apply(clean_list)

    # --- Safely parse team_size ---
    def clean_team_size(t):
        try:
            if pd.isnull(t):
                return 0
            return int(str(t).replace(",", "").strip())
        except:
            return 0

    df['team_size'] = df['team_size'].apply(clean_team_size)

    # --- Drop duplicates on name ---
    df.drop_duplicates(subset='name', inplace=True)

    # --- Save to CSV ---
    os.makedirs("./data/processed", exist_ok=True)
    df.to_csv("./data/processed/yc_clean.csv", index=False, quotechar='"', quoting=csv.QUOTE_ALL)

    # --- Print contents ---
    print(df.head())

if __name__ == "__main__":
    transform_yc_data()