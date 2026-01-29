from src.data_loader import load_data
from src.model import MatchPredictor

THRESHOLD = 0.55  # final tuned threshold

def main():
    # Load historical data
    matches = load_data()

    # Train final model (binary, odds + form)
    predictor = MatchPredictor()
    predictor.train(matches)

    # Example fixture
    home = "Man Utd"
    away = "Fulham"

    result = predictor.predict_match(home, away)
    p_home = result["home_win"]
    p_away = 1 - p_home

    decision = home if p_home >= THRESHOLD else away

    print(f"\n{home} vs {away}")
    print(f"{home}: {p_home:.3f}")
    print(f"{away}: {p_away:.3f}")
    print(f"Prediction (τ = {THRESHOLD}): {decision}")

    

if __name__ == "__main__":
    main()
