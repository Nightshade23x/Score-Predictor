DATA_PATH = "data/raw"

WINDOW_SIZE = 5
H2H_WINDOW = 5

TRAIN_SPLIT = 0.8

FEATURES = [
    # Form features
    "home_points_last5",
    "home_goals_scored_last5",
    "home_goals_conceded_last5",
    "away_points_last5",
    "away_goals_scored_last5",
    "away_goals_conceded_last5",

    # Head-to-head features
    "h2h_points_home_last5",
    "h2h_points_away_last5",
    "h2h_goal_diff_home_last5",
]

LABEL_MAP = {"H": 2, "D": 1, "A": 0}
