import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier

from src.config import FEATURES, LABEL_MAP
from src.feature_engineering import add_form_features


class GBMatchPredictor:
    def __init__(self):
        self.model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=2,
            min_samples_leaf=20,
            random_state=42
        )
        self.history = None

    def train(self, matches):
        matches = matches.copy()

        # Create target
        matches["target"] = matches["FTR"].map(LABEL_MAP)

        # Feature engineering
        matches = add_form_features(matches)

        X = matches[FEATURES]
        y = matches["target"]

        self.model.fit(X, y)
        self.history = matches.copy()

    def predict_match(self, home_team, away_team):
        if self.history is None:
            raise RuntimeError("Model must be trained before prediction")

        future_match = pd.DataFrame([{
            "HomeTeam": home_team,
            "AwayTeam": away_team,
            "FTR": "D",   # dummy
            "FTHG": 0,
            "FTAG": 0
        }])

        combined = pd.concat([self.history, future_match], ignore_index=True)
        combined = add_form_features(combined)

        X_match = combined.iloc[-1:][FEATURES]

        probs = self.model.predict_proba(X_match)[0]
        classes = self.model.classes_

        prob_map = dict(zip(classes, probs))

        return {
            "home_win": prob_map[LABEL_MAP["H"]],
            "draw": prob_map[LABEL_MAP["D"]],
            "away_win": prob_map[LABEL_MAP["A"]],
            "prediction": max(
                [("Home Win", prob_map[LABEL_MAP["H"]]),
                 ("Draw", prob_map[LABEL_MAP["D"]]),
                 ("Away Win", prob_map[LABEL_MAP["A"]])],
                key=lambda x: x[1]
            )[0]
        }
