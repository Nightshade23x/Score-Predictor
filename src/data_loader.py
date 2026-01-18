import os
import pandas as pd
from src.config import DATA_PATH

def load_data():
    files = [f for f in os.listdir(DATA_PATH) if f.endswith(".csv")]

    dfs = []
    for file in files:
        df = pd.read_csv(os.path.join(DATA_PATH, file))
        dfs.append(df)

    matches = pd.concat(dfs, ignore_index=True)

    matches = matches[
        ["Date", "HomeTeam", "AwayTeam", "FTR", "FTHG", "FTAG"]
    ]

    matches["Date"] = pd.to_datetime(matches["Date"], dayfirst=True)
    matches = matches.sort_values("Date").reset_index(drop=True)

    return matches
