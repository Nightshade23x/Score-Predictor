from src.config import WINDOW_SIZE

def get_points(result, is_home):
    if result == "D":
        return 1
    if result == "H" and is_home:
        return 3
    if result == "A" and not is_home:
        return 3
    return 0

def add_form_features(matches):
    team_history = {}

    home_points = []
    home_goals_scored = []
    home_goals_conceded = []

    away_points = []
    away_goals_scored = []
    away_goals_conceded = []

    for _, row in matches.iterrows():
        home = row["HomeTeam"]
        away = row["AwayTeam"]

        for team in [home, away]:
            if team not in team_history:
                team_history[team] = []

        home_past = team_history[home][-WINDOW_SIZE:]
        away_past = team_history[away][-WINDOW_SIZE:]

        home_points.append(sum(m["points"] for m in home_past))
        home_goals_scored.append(sum(m["goals_scored"] for m in home_past))
        home_goals_conceded.append(sum(m["goals_conceded"] for m in home_past))

        away_points.append(sum(m["points"] for m in away_past))
        away_goals_scored.append(sum(m["goals_scored"] for m in away_past))
        away_goals_conceded.append(sum(m["goals_conceded"] for m in away_past))

        team_history[home].append({
            "points": get_points(row["FTR"], True),
            "goals_scored": row["FTHG"],
            "goals_conceded": row["FTAG"]
        })

        team_history[away].append({
            "points": get_points(row["FTR"], False),
            "goals_scored": row["FTAG"],
            "goals_conceded": row["FTHG"]
        })

    matches["home_points_last5"] = home_points
    matches["home_goals_scored_last5"] = home_goals_scored
    matches["home_goals_conceded_last5"] = home_goals_conceded

    matches["away_points_last5"] = away_points
    matches["away_goals_scored_last5"] = away_goals_scored
    matches["away_goals_conceded_last5"] = away_goals_conceded

    return matches
