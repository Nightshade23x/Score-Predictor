import os

# -------- Paths --------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data","raw")

# -------- Windows --------
WINDOW_SIZE = 5
H2H_WINDOW = 5

# -------- Labels --------
LABEL_MAP = {
    "A": 0,
    "D": 1,
    "H": 2
}

# -------- Big teams (kept for later experiments) --------
BIG_TEAMS = {
    "Man City",
    "Liverpool",
    "Arsenal",
    "Chelsea",
    "Man United",
    "Tottenham"
}

# -------- FEATURES: STATS-ONLY BASELINE --------
# -------- FEATURES: DIFFERENTIALS-ONLY BASELINE --------
FEATURES = [
    "form_points_diff",
    "form_goal_diff_diff",
    "season_strength_diff",
    "h2h_points_diff",
]
