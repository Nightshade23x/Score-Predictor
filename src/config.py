DATA_DIR="data/raw"
WINDOW_SIZE=5
H2H_WINDOW=5
BIG_TEAMS = [
    "Man City",
    "Liverpool",
    "Arsenal",
    "Chelsea",
    "Tottenham"
]

FEATURES = [
    "home_points_lastN",
    "home_goals_scored_lastN",
    "home_goals_conceded_lastN",
    "home_goal_diff_lastN",
    "home_matches_lastN",

    "away_points_lastN",
    "away_goals_scored_lastN",
    "away_goals_conceded_lastN",
    "away_goal_diff_lastN",
    "away_matches_lastN",

    "home_season_strength",
    "away_season_strength",

    "home_vs_big",
    "away_vs_big",
    "man_utd_vs_big",

    "h2h_points_home_lastN",
    "h2h_points_away_lastN",
    "h2h_goal_diff_home_lastN",
    "h2h_matches_lastN",
]
LABEL_MAP = {
    "A": 0,
    "D": 1,
    "H": 2
}
