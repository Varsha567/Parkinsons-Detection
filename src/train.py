import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier

df = pd.read_csv(
    "data/parkinsons/parkinsons.data"
)

X = df.drop(
    ["name", "status"],
    axis=1
)

y = df["status"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = XGBClassifier(
    random_state=42
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

print(classification_report(y_test, pred))
print("Accuracy:", accuracy_score(y_test, pred))

joblib.dump(
    model,
    "models/xgboost_model.pkl"
)

print("Model saved!")