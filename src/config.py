DATA_PATH = "data/raw"
WINDOW_SIZE = 5
TRAIN_SPLIT = 0.8

FEATURES = [
    "home_points_last5",
    "home_goals_scored_last5",
    "home_goals_conceded_last5",
    "away_points_last5",
    "away_goals_scored_last5",
    "away_goals_conceded_last5",
]

LABEL_MAP = {"H": 2, "D": 1, "A": 0}
