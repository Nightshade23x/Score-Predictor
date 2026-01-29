import pandas as pd
from sklearn.metrics import accuracy_score, log_loss, brier_score_loss

from src.data_loader import load_data
from src.model import MatchPredictor
from src.config import FEATURES


def backtest_by_season():
    THRESHOLD=0.60
    data = load_data()

    # IMPORTANT: ensure chronological order
    data = data.sort_values(["season"]).reset_index(drop=True)

    seasons = sorted(data["season"].unique())

    results = []

    # Train on seasons < test_season, test on test_season
    for i in range(1, len(seasons)):
        train_seasons = seasons[:i]
        test_season = seasons[i]

        train_data = data[data["season"].isin(train_seasons)]
        test_data = data[data["season"] == test_season]

        predictor = MatchPredictor()
        predictor.train(train_data)

        y_true = []
        y_pred = []
        y_prob = []

        for _, row in test_data.iterrows():
            pred = predictor.predict_match(row["HomeTeam"], row["AwayTeam"])

            y_true.append(1 if row["FTR"] == "H" else 0)
            y_prob.append(pred["home_win"])
            y_pred.append(1 if pred["home_win"] >= THRESHOLD else 0)



        # Map labels for metrics
        

        acc = accuracy_score(y_true, y_pred)
        ll = log_loss(y_true, [[1-p, p] for p in y_prob])


        results.append({
            "train_up_to": train_seasons[-1],
            "test_season": test_season,
            "accuracy": round(acc, 3),
            "log_loss": round(ll, 3)
        })

        print(
            f"Train ≤ {train_seasons[-1]} | "
            f"Test {test_season} | "
            f"Acc: {acc:.3f} | "
            f"LogLoss: {ll:.3f}"
        )

    return pd.DataFrame(results)

def inspect_coefficients():
    """
    Train on all data and print model coefficients (binary).
    """
    data = load_data()
    data = data.sort_values(["season"]).reset_index(drop=True)

    predictor = MatchPredictor()
    predictor.train(data)

    coef_df = predictor.get_coefficients()

    print("\n=== COEFFICIENTS (Home Win vs Not Home Win) ===")
    print(
        coef_df.sort_values("coefficient", ascending=False)
    )




if __name__ == "__main__":
    df_results = backtest_by_season()
    print("\nOverall results:")
    print(df_results)

    #inspect_coefficients()

