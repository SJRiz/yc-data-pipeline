import json
import csv
import pandas as pd
import os

def transform_yc_data():
    # Load raw JSON
    with open("./data/raw/yc_raw.json", "r", encoding="utf-8") as f:
        raw = json.load(f)
    df = pd.DataFrame(raw)

    # Clean up list‐columns and format them as Postgres arrays
    def clean_list_to_pg_array(L):
        if isinstance(L, list):
            # lower‐case, strip commas/spaces
            items = [str(t).strip().lower() for t in L if isinstance(t, str)]

            # join with commas, wrap in {}
            return "{" + ",".join(items) + "}"
        return "{}"

    df['tags']       = df['tags'].apply(clean_list_to_pg_array)
    df['industries'] = df['industries'].apply(clean_list_to_pg_array)

    # Clean team_size
    def clean_team_size(t):
        try:
            if pd.isnull(t): return 0
            ts = str(t).replace(",", "").strip()
            return int(float(ts))
        except:
            return 0
        
    df['team_size'] = df['team_size'].apply(clean_team_size)

    # Convert funding == 0 to None
    def clean_funding(val):
        try:
            val = int(str(val).replace(',', '').strip())
            return None if val == 0 else val
        except:
            return None
        
    df['funding'] = df['funding'].apply(clean_funding)

    # Convert booleans into lowercase literal strings
    df['eng']    = df['eng'].astype(bool).map(lambda b: 'true' if b else 'false')
    df['remote'] = df['remote'].astype(bool).map(lambda b: 'true' if b else 'false')

    # Drop duplicates and ensure processed folder exists
    df.drop_duplicates(subset='name', inplace=True)
    os.makedirs("./data/processed", exist_ok=True)

    pg_cols = [
        "name","slug","ceo_name","ceo_linkedin","company_linkedin",
        "eng","remote","job_website","description","stage",
        "tags","industries","all_locations","team_size","batch","funding"
    ]
    
    df.to_csv(
        "./data/processed/yc_clean.csv",
        columns=pg_cols,
        index=False,
        quotechar='"',
        quoting=csv.QUOTE_ALL,
        na_rep=''
    )