from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from src.config import FEATURES, LABEL_MAP, TRAIN_SPLIT

def train_and_evaluate(matches):
    matches["target"] = matches["FTR"].map(LABEL_MAP)

    X = matches[FEATURES]
    y = matches["target"]

    split = int(len(matches) * TRAIN_SPLIT)

    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]

    model = LogisticRegression(
        max_iter=1000
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print("\nMODEL PERFORMANCE")
    print("-----------------")
    print("Accuracy:", round(accuracy_score(y_test, y_pred) * 100, 2), "%\n")

    print("Confusion Matrix (A, D, H):")
    print(confusion_matrix(y_test, y_pred))

    print("\nClassification Report:")
    print(classification_report(
        y_test,
        y_pred,
        target_names=["Away Win", "Draw", "Home Win"]
    ))
