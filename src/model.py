import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.config import FEATURES, LABEL_MAP
from src.feature_engineering import add_form_features


class MatchPredictor:
    def __init__(self):
        # Pipeline = scaling + logistic regression
        self.model = Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=1000))
        ])

    def train(self, matches):
        matches = matches.copy()

        # Create target
        matches["target"] = matches["FTR"].map(LABEL_MAP)

        # Create features
        matches = add_form_features(matches)

        X = matches[FEATURES]
        y = matches["target"]

        self.model.fit(X, y)

    def predict_match(self, home_team, away_team):
        # Dummy row to generate features
        row = {
            "HomeTeam": home_team,
            "AwayTeam": away_team,
            "FTR": "D",   # dummy
            "FTHG": 0,    # dummy
            "FTAG": 0     # dummy
        }

        df = pd.DataFrame([row])

        # Generate features using SAME pipeline
        df = add_form_features(df)

        X_match = df[FEATURES]

        probs = self.model.predict_proba(X_match)[0]

        return {
            "home_win": probs[2],
            "draw": probs[1],
            "away_win": probs[0],
            "prediction": ["Away Win", "Draw", "Home Win"][probs.argmax()]
        }
