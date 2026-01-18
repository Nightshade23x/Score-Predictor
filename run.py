from src.data_loader import load_data
from src.feature_engineering import add_form_features
from src.model import MatchPredictor

def main():
    # Load and prepare data
    matches = load_data()
    matches = add_form_features(matches)

    # Train predictor
    predictor = MatchPredictor()
    predictor.train(matches)

    # Example prediction: Man United vs Man City
    home = "Man United"
    away = "Man City"

    result = predictor.predict_match(home, away)

    print(f"\n{home} vs {away}")
    print(f"Home win: {result['home_win']:.2f}")
    print(f"Draw: {result['draw']:.2f}")
    print(f"Away win: {result['away_win']:.2f}")
    print("Predicted result:", result["prediction"])

if __name__ == "__main__":
    main()
