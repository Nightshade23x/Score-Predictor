from src.data_loader import load_data
from src.feature_engineering import add_form_features
from src.model import train_and_evaluate

def main():
    matches = load_data()
    matches = add_form_features(matches)
    train_and_evaluate(matches)

if __name__ == "__main__":
    main()
