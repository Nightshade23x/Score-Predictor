from src.config import WINDOW_SIZE, H2H_WINDOW

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
    h2h_history = {}

    home_points = []
    home_goals_scored = []
    home_goals_conceded = []

    away_points = []
    away_goals_scored = []
    away_goals_conceded = []

    h2h_home_points = []
    h2h_away_points = []
    h2h_home_goal_diff = []

    for _, row in matches.iterrows():
        home = row["HomeTeam"]
        away = row["AwayTeam"]

        # ---------- Team history ----------
        for team in [home, away]:
            if team not in team_history:
                team_history[team] = []

        home_past = team_history[home][-WINDOW_SIZE:]
        away_past = team_history[away][-WINDOW_SIZE:]

        home_points.append(sum(m["points"] for m in home_past))
        home_goals_scored.append(sum(m["scored"] for m in home_past))
        home_goals_conceded.append(sum(m["conceded"] for m in home_past))

        away_points.append(sum(m["points"] for m in away_past))
        away_goals_scored.append(sum(m["scored"] for m in away_past))
        away_goals_conceded.append(sum(m["conceded"] for m in away_past))

        # ---------- Head-to-head history ----------
        pair = tuple(sorted([home, away]))
        if pair not in h2h_history:
            h2h_history[pair] = []

        h2h_past = h2h_history[pair][-H2H_WINDOW:]

        home_pts = 0
        away_pts = 0
        home_gd = 0

        for m in h2h_past:
            if m["home"] == home:
                home_pts += m["home_points"]
                away_pts += m["away_points"]
                home_gd += m["home_goals"] - m["away_goals"]
            else:
                home_pts += m["away_points"]
                away_pts += m["home_points"]
                home_gd += m["away_goals"] - m["home_goals"]

        h2h_home_points.append(home_pts)
        h2h_away_points.append(away_pts)
        h2h_home_goal_diff.append(home_gd)

        # ---------- Update histories AFTER match ----------
        team_history[home].append({
            "points": get_points(row["FTR"], True),
            "scored": row["FTHG"],
            "conceded": row["FTAG"]
        })

        team_history[away].append({
            "points": get_points(row["FTR"], False),
            "scored": row["FTAG"],
            "conceded": row["FTHG"]
        })

        h2h_history[pair].append({
            "home": home,
            "away": away,
            "home_points": get_points(row["FTR"], True),
            "away_points": get_points(row["FTR"], False),
            "home_goals": row["FTHG"],
            "away_goals": row["FTAG"]
        })

    # ---------- Attach features ----------
    matches["home_points_last5"] = home_points
    matches["home_goals_scored_last5"] = home_goals_scored
    matches["home_goals_conceded_last5"] = home_goals_conceded

    matches["away_points_last5"] = away_points
    matches["away_goals_scored_last5"] = away_goals_scored
    matches["away_goals_conceded_last5"] = away_goals_conceded

    matches["h2h_points_home_last5"] = h2h_home_points
    matches["h2h_points_away_last5"] = h2h_away_points
    matches["h2h_goal_diff_home_last5"] = h2h_home_goal_diff

    return matches
