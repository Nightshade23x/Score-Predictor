import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.config import FEATURES, LABEL_MAP
from src.feature_engineering import add_form_features


class MatchPredictor:
    def __init__(self):
        self.model = Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=1000))
        ])
        self.history = None  # store training data

    def train(self, matches):
        matches = matches.copy()

        # Create target
        matches["target"] = matches["FTR"].map(LABEL_MAP)

        # Generate features using full history
        matches = add_form_features(matches)

        X = matches[FEATURES]
        y = matches["target"]

        self.model.fit(X, y)

        # Save history for future predictions
        self.history = matches.copy()

    def predict_match(self, home_team, away_team):
        if self.history is None:
            raise RuntimeError("Model must be trained before prediction")

        # Create future match (dummy result/goals)
        future_match = pd.DataFrame([{
            "HomeTeam": home_team,
            "AwayTeam": away_team,
            "FTR": "D",   # dummy
            "FTHG": 0,    # dummy
            "FTAG": 0     # dummy
        }])

        # Append to historical data
        combined = pd.concat([self.history, future_match], ignore_index=True)

        # Regenerate features INCLUDING history
        combined = add_form_features(combined)

        # Extract features for the future match
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
    def predict_proba_match(self, home_team, away_team):
        pred = self.predict_match(home_team, away_team)
        return [
            pred["away_win"],
            pred["draw"],
            pred["home_win"]
        ]
    def get_coefficients(self):
        """
        Returns a DataFrame of coefficients for each class.
        """
        clf = self.model.named_steps["clf"]
        scaler = self.model.named_steps["scaler"]

        # Feature names
        features = self.model.feature_names_in_

        # Coefficients after scaling
        coefs = clf.coef_

        # Classes: 0 = Away, 1 = Draw, 2 = Home
        rows = []
        for class_idx, class_label in enumerate(clf.classes_):
            for feat, coef in zip(features, coefs[class_idx]):
                rows.append({
                    "class": class_label,
                    "feature": feat,
                    "coefficient": coef
                })

        return pd.DataFrame(rows)


