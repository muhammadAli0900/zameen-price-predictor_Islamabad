# src/training_prediction_model.py

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# --- Paths (robust to where you run from) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "cleaned", "zameen_islamabad_model_ready.csv")
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")
MODEL_PATH = os.path.join(MODEL_DIR, "best_model.pkl")

# --- Load data ---
df = pd.read_csv(DATA_PATH)

# Target & features (no 'Area', no 'Price Per Marla')
TARGET = "Price (PKR)"
FEATURES = ["Beds", "Baths", "Area (Marla)", "Block", "Phase", "Sector"]

# Drop rows with missing target for training
df = df.dropna(subset=[TARGET])

# Split X / y
X = df[FEATURES]
y = df[TARGET]

# Feature groups
numeric_features = ["Beds", "Baths", "Area (Marla)"]
categorical_features = ["Block", "Phase", "Sector"]

# Preprocessing
numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median"))
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features),
    ],
    remainder="drop",
)

# Model pipeline
pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", RandomForestRegressor(n_estimators=300, random_state=42, n_jobs=-1)),
])

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Fit
pipeline.fit(X_train, y_train)

# Evaluate
y_pred = pipeline.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("✅ Model Trained and Evaluated")
print(f"📉 MAE:  {mae:,.2f}")
print(f"📉 RMSE: {rmse:,.2f}")
print(f"📈 R²:   {r2:.4f}")

# Save
os.makedirs(MODEL_DIR, exist_ok=True)
joblib.dump(pipeline, MODEL_PATH)
print(f"✅ Model pipeline saved to {MODEL_PATH}")
