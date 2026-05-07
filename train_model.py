import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Example dataset
df = pd.read_csv("data.csv")

# 🔴 IMPORTANT: define feature columns explicitly
feature_cols = ["age", "salary", "experience", "gender_encoded"]


X = df[feature_cols]
y = df["target"]

# train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# save feature order for prediction use
import joblib
joblib.dump(model, "model.pkl")
joblib.dump(feature_cols, "features.pkl")