import os
import pandas as pd
from src.config import DATA_DIR


def load_data():
    dfs = []

    for file in sorted(os.listdir(DATA_DIR)):
        if file.endswith(".csv"):
            path = os.path.join(DATA_DIR, file)
            df = pd.read_csv(path)

            if df.empty:
                continue

            df.columns = df.columns.str.strip()
            df["season"] = file.replace(".csv", "")

            dfs.append(df)

    if not dfs:
        raise RuntimeError("No CSV files found in DATA_DIR")

    data = pd.concat(dfs, ignore_index=True)
    return data
