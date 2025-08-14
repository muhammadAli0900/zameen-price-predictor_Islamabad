# src/evalute_model.py

import os
import joblib
import numpy as pd
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "best_model.pkl")
TEST_DATA_PATH = os.path.join(BASE_DIR, "..", "data", "cleaned", "zameen_islamabad_model_ready.csv")
PREDICTIONS_PATH = os.path.join(BASE_DIR, "..", "data", "processed", "predictions.csv")

# --- Must match training FEATURES exactly ---
FEATURES = ["Beds", "Baths", "Area (Marla)", "Block", "Phase", "Sector"]
TARGET = "Price (PKR)"

print("Loading test dataset...")
df = pd.read_csv(TEST_DATA_PATH)

# Ensure all required feature columns exist
missing_cols = set(FEATURES) - set(df.columns)
if missing_cols:
    raise ValueError(f"Missing required feature columns in test data: {missing_cols}")

# Drop rows with missing target for metric calculation (keep a copy if you want preds for all)
df_eval = df.dropna(subset=[TARGET]).copy()

X = df_eval[FEATURES]
y = df_eval[TARGET]

print("Loading trained model...")
model = joblib.load(MODEL_PATH)

print("Making predictions...")
y_pred = model.predict(X)

# Metrics
mae = mean_absolute_error(y, y_pred)
rmse = np.sqrt(mean_squared_error(y, y_pred))
r2 = r2_score(y, y_pred)

print("\n📊 Model Evaluation on Provided Data:")
print(f"MAE : {mae:,.2f}")
print(f"RMSE: {rmse:,.2f}")
print(f"R²  : {r2:.4f}")

# Save predictions (with actuals for rows that had target)
os.makedirs(os.path.dirname(PREDICTIONS_PATH), exist_ok=True)
out = df_eval.copy()
out["Predicted Price (PKR)"] = y_pred
out.to_csv(PREDICTIONS_PATH, index=False)
print(f"\n✅ Predictions (with actuals) saved to: {PREDICTIONS_PATH}")
