import pandas as pd
import joblib

# Load trained model
model = joblib.load("../models/best_model.pkl")  # adjust path if needed

# Take inputs
size = float(input("Enter size in marla: "))
beds = int(input("Enter number of bedrooms: "))
baths = int(input("Enter number of bathrooms: "))
sector = input("Enter sector (e.g., I-8): ").strip().upper()

# Default/fallback values for missing features
phase = "Unknown"
block = "Unknown"

# Create DataFrame with the exact same columns as training
X_new = pd.DataFrame([{
    "Area (Marla)": size,
    "Beds": beds,
    "Baths": baths,
    "Sector": sector,
    "Phase": phase,
    "Block": block
}])

# Predict
predicted_price = model.predict(X_new)[0]
print(f"Predicted Price: {predicted_price:,.0f} PKR")
