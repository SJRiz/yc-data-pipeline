from .utils.scraper import fetch_yc_companies
from itertools import islice
from libs.app_config.config import COMPANIES_PER_EXTRACT
import os, json

def extract_yc_data():

    os.makedirs("data/raw", exist_ok=True)
    data = list(islice(fetch_yc_companies(), COMPANIES_PER_EXTRACT))

    with open('data/raw/yc_raw.json', 'w') as f:
        json.dump(data, f, indent=4)

    # Print the extracted data as formatted JSON string
    print(json.dumps(data, indent=4))

if __name__ == "__main__":
    extract_yc_data()