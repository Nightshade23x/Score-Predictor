import pandas as pd
from sklearn.metrics import accuracy_score, log_loss, brier_score_loss

from src.data_loader import load_data
from src.model_gb import GBMatchPredictor
from src.config import FEATURES


def backtest_by_season():
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

        predictor = GBMatchPredictor()
        predictor.train(train_data)

        y_true = []
        y_pred = []
        y_prob = []

        for _, row in test_data.iterrows():
            pred = predictor.predict_match(row["HomeTeam"], row["AwayTeam"])

            y_true.append(row["FTR"])
            y_pred.append(
                "H" if pred["prediction"] == "Home Win"
                else "D" if pred["prediction"] == "Draw"
                else "A"
            )
            y_prob.append([
                pred["away_win"],
                pred["draw"],
                pred["home_win"]
            ])

        # Map labels for metrics
        label_map = {"A": 0, "D": 1, "H": 2}
        y_true_num = [label_map[x] for x in y_true]
        y_pred_num = [label_map[x] for x in y_pred]

        acc = accuracy_score(y_true_num, y_pred_num)
        ll = log_loss(y_true_num, y_prob, labels=[0, 1, 2])

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

#def inspect_coefficients():
    """
    Train on all data and print model coefficients.
    """
    data = load_data()

    # Ensure chronological order
    data = data.sort_values(["season"]).reset_index(drop=True)

    predictor = GBMatchPredictor()
    predictor.train(data)

    coef_df = predictor.get_coefficients()

    print("\n=== TOP POSITIVE COEFFICIENTS (Home Win) ===")
    print(
        coef_df[coef_df["class"] == 2]
        .sort_values("coefficient", ascending=False)
        .head(10)
    )

    print("\n=== TOP NEGATIVE COEFFICIENTS (Away Win) ===")
    print(
        coef_df[coef_df["class"] == 0]
        .sort_values("coefficient")
        .head(10)
    )



if __name__ == "__main__":
    df_results = backtest_by_season()
    print("\nOverall results:")
    print(df_results)

    #inspect_coefficients()

