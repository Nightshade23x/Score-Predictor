from src.config import WINDOW_SIZE, H2H_WINDOW, BIG_TEAMS


def get_points(result, is_home):
    if result == "D":
        return 1
    if result == "H" and is_home:
        return 3
    if result == "A" and not is_home:
        return 3
    return 0


def safe_avg(values):
    return sum(values) / len(values) if values else 0


def add_form_features(matches):
    team_history = {}
    h2h_history = {}

    # -------- Core form features --------
    home_points = []
    home_goals_scored = []
    home_goals_conceded = []
    home_goal_diff = []
    home_matches = []

    away_points = []
    away_goals_scored = []
    away_goals_conceded = []
    away_goal_diff = []
    away_matches = []

    # -------- H2H --------
    h2h_home_points = []
    h2h_away_points = []
    h2h_home_goal_diff = []
    h2h_matches = []

    # -------- New pattern features --------
    home_vs_big = []
    away_vs_big = []
    man_utd_vs_big = []

    home_season_strength = []
    away_season_strength = []

    for _, row in matches.iterrows():
        home = row["HomeTeam"]
        away = row["AwayTeam"]

        for team in [home, away]:
            if team not in team_history:
                team_history[team] = []

        # -------- Home / Away recent form --------
        home_past = [m for m in team_history[home] if m["is_home"]][-WINDOW_SIZE:]
        away_past = [m for m in team_history[away] if not m["is_home"]][-WINDOW_SIZE:]

        home_points.append(safe_avg([m["points"] for m in home_past]))
        home_goals_scored.append(safe_avg([m["scored"] for m in home_past]))
        home_goals_conceded.append(safe_avg([m["conceded"] for m in home_past]))
        home_goal_diff.append(safe_avg([m["scored"] - m["conceded"] for m in home_past]))
        home_matches.append(len(home_past))

        away_points.append(safe_avg([m["points"] for m in away_past]))
        away_goals_scored.append(safe_avg([m["scored"] for m in away_past]))
        away_goals_conceded.append(safe_avg([m["conceded"] for m in away_past]))
        away_goal_diff.append(safe_avg([m["scored"] - m["conceded"] for m in away_past]))
        away_matches.append(len(away_past))

        # -------- Season-long home strength (pattern: Newcastle, Villa, Liverpool) --------
        home_all = [m for m in team_history[home] if m["is_home"]]
        away_all = [m for m in team_history[away] if not m["is_home"]]

        home_season_strength.append(safe_avg([m["points"] for m in home_all]))
        away_season_strength.append(safe_avg([m["points"] for m in away_all]))

        # -------- Big team patterns --------
        home_vs_big.append(1 if away in BIG_TEAMS else 0)
        away_vs_big.append(1 if home in BIG_TEAMS else 0)

        man_utd_vs_big.append(
            1 if home == "Man United" and away in BIG_TEAMS else 0
        )

        # -------- Head-to-head --------
        pair = tuple(sorted([home, away]))
        if pair not in h2h_history:
            h2h_history[pair] = []

        h2h_past = h2h_history[pair][-H2H_WINDOW:]

        hp, ap, gd, w_sum = 0, 0, 0, 0
        for i, m in enumerate(h2h_past):
            w = i + 1
            w_sum += w

            if m["home"] == home:
                hp += w * m["home_points"]
                ap += w * m["away_points"]
                gd += w * (m["home_goals"] - m["away_goals"])
            else:
                hp += w * m["away_points"]
                ap += w * m["home_points"]
                gd += w * (m["away_goals"] - m["home_goals"])

        h2h_home_points.append(hp / w_sum if w_sum else 0)
        h2h_away_points.append(ap / w_sum if w_sum else 0)
        h2h_home_goal_diff.append(gd / w_sum if w_sum else 0)
        h2h_matches.append(len(h2h_past))

        # -------- Update histories AFTER match --------
        team_history[home].append({
            "points": get_points(row["FTR"], True),
            "scored": row["FTHG"],
            "conceded": row["FTAG"],
            "is_home": True
        })

        team_history[away].append({
            "points": get_points(row["FTR"], False),
            "scored": row["FTAG"],
            "conceded": row["FTHG"],
            "is_home": False
        })

        h2h_history[pair].append({
            "home": home,
            "away": away,
            "home_points": get_points(row["FTR"], True),
            "away_points": get_points(row["FTR"], False),
            "home_goals": row["FTHG"],
            "away_goals": row["FTAG"]
        })

    # -------- Attach features --------
    matches["home_points_lastN"] = home_points
    matches["home_goals_scored_lastN"] = home_goals_scored
    matches["home_goals_conceded_lastN"] = home_goals_conceded
    matches["home_goal_diff_lastN"] = home_goal_diff
    matches["home_matches_lastN"] = home_matches

    matches["away_points_lastN"] = away_points
    matches["away_goals_scored_lastN"] = away_goals_scored
    matches["away_goals_conceded_lastN"] = away_goals_conceded
    matches["away_goal_diff_lastN"] = away_goal_diff
    matches["away_matches_lastN"] = away_matches

    matches["home_season_strength"] = home_season_strength
    matches["away_season_strength"] = away_season_strength

    matches["home_vs_big"] = home_vs_big
    matches["away_vs_big"] = away_vs_big
    matches["man_utd_vs_big"] = man_utd_vs_big

    matches["h2h_points_home_lastN"] = h2h_home_points
    matches["h2h_points_away_lastN"] = h2h_away_points
    matches["h2h_goal_diff_home_lastN"] = h2h_home_goal_diff
    matches["h2h_matches_lastN"] = h2h_matches

    return matches
