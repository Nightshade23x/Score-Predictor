from sklearn.linear_model import LogisticRegression
from src.config import FEATURES, LABEL_MAP, H2H_WINDOW

class MatchPredictor:
    def __init__(self):
        self.model = LogisticRegression(max_iter=1000)
        self.team_form = {}
        self.h2h_history = {}

    def train(self, matches):
        matches = matches.copy()
        matches["target"] = matches["FTR"].map(LABEL_MAP)

        X = matches[FEATURES]
        y = matches["target"]

        # Train on all data
        self.model.fit(X, y)

        # Build histories for prediction
        self._build_histories(matches)

    def _build_histories(self, matches):
        self.team_form = {}
        self.h2h_history = {}

        for _, row in matches.iterrows():
            home = row["HomeTeam"]
            away = row["AwayTeam"]

            # ---- team form ----
            for team in [home, away]:
                if team not in self.team_form:
                    self.team_form[team] = []

            self.team_form[home].append({
                "points": self._get_points(row["FTR"], True),
                "scored": row["FTHG"],
                "conceded": row["FTAG"]
            })

            self.team_form[away].append({
                "points": self._get_points(row["FTR"], False),
                "scored": row["FTAG"],
                "conceded": row["FTHG"]
            })

            # ---- head to head ----
            pair = tuple(sorted([home, away]))
            if pair not in self.h2h_history:
                self.h2h_history[pair] = []

            self.h2h_history[pair].append({
                "home": home,
                "away": away,
                "home_points": self._get_points(row["FTR"], True),
                "away_points": self._get_points(row["FTR"], False),
                "home_goals": row["FTHG"],
                "away_goals": row["FTAG"]
            })

    def _get_points(self, result, is_home):
        if result == "D":
            return 1
        if result == "H" and is_home:
            return 3
        if result == "A" and not is_home:
            return 3
        return 0

    def _get_last5_form(self, team):
        history = self.team_form.get(team, [])[-5:]
        return [
            sum(m["points"] for m in history),
            sum(m["scored"] for m in history),
            sum(m["conceded"] for m in history),
        ]

    def _get_h2h_features(self, home, away):
        pair = tuple(sorted([home, away]))
        history = self.h2h_history.get(pair, [])[-H2H_WINDOW:]

        home_pts = 0
        away_pts = 0
        home_gd = 0

        for m in history:
            if m["home"] == home:
                home_pts += m["home_points"]
                away_pts += m["away_points"]
                home_gd += m["home_goals"] - m["away_goals"]
            else:
                home_pts += m["away_points"]
                away_pts += m["home_points"]
                home_gd += m["away_goals"] - m["home_goals"]

        return [home_pts, away_pts, home_gd]

    def predict_match(self, home_team, away_team):
        home_form = self._get_last5_form(home_team)
        away_form = self._get_last5_form(away_team)
        h2h_feats = self._get_h2h_features(home_team, away_team)

        X_match = [home_form + away_form + h2h_feats]

        probs = self.model.predict_proba(X_match)[0]

        return {
            "home_win": probs[2],
            "draw": probs[1],
            "away_win": probs[0],
            "prediction": ["Away Win", "Draw", "Home Win"][probs.argmax()]
        }
