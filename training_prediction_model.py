import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# Load dataset
df = pd.read_csv("zameen_islamabad_model_ready.csv")

# Drop rows with missing target
df.dropna(subset=["Price (PKR)"], inplace=True)

# Fill missing values in location attributes
location_columns = ["Area", "Block", "Phase", "Sector"]
df[location_columns] = df[location_columns].fillna("Unknown")

# Define features and target
X = df[["Beds", "Baths", "Area (Marla)", "Area", "Block", "Phase", "Sector"]]
y = df["Price (PKR)"]

# Preprocessing pipeline for categorical features
categorical_features = ["Area", "Block", "Phase", "Sector"]
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ],
    remainder="passthrough"  # Keep numerical features
)

# Full pipeline with model
model_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
])

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model_pipeline.fit(X_train, y_train)

# Predictions
y_pred = model_pipeline.predict(X_test)

# Evaluation
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

# Show evaluation results
print("✅ Model Trained and Evaluated")
print(f"📉 MAE: {mae:,.2f}")
print(f"📉 RMSE: {rmse:,.2f}")
print(f"📈 R² Score: {r2:.4f}")
