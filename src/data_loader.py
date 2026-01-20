import os
import pandas as pd
from src.config import DATA_DIR


def load_data():
    dfs = []

    for file in os.listdir(DATA_DIR):
        if file.endswith(".csv"):
            path = os.path.join(DATA_DIR, file)
            df = pd.read_csv(path)
            dfs.append(df)

    data = pd.concat(dfs, ignore_index=True)
    return data
