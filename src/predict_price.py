# predict_price.py
import joblib
import pandas as pd
import os

# Paths
MODEL_PATH = os.path.join("..", "models", "best_model.pkl")
DATA_PATH = os.path.join("..", "data", "cleaned", "zameen_islamabad_model_ready.csv")

# Load model and dataset
model = joblib.load(MODEL_PATH)
df = pd.read_csv(DATA_PATH)

# Get user input
area = float(input("Enter property size in Marla: "))
beds = int(input("Enter number of bedrooms: "))
baths = int(input("Enter number of bathrooms: "))
sector = input("Enter sector (e.g., F-10, G-13): ").strip()

# Calculate average Price Per Marla for that sector
sector_data = df[df['Sector'].str.strip().str.lower() == sector.lower()]

if sector_data.empty:
    print(f"No data found for sector '{sector}'. Using overall average Price Per Marla.")
    price_per_marla = df['Price Per Marla'].mean()
    block = df['Block'].mode()[0]
    phase = df['Phase'].mode()[0]
else:
    price_per_marla = sector_data['Price Per Marla'].mean()
    block = sector_data['Block'].mode()[0]
    phase = sector_data['Phase'].mode()[0]

# Create input DataFrame for prediction
new_property = pd.DataFrame([{
    'Beds': beds,
    'Baths': baths,
    'Area (Marla)': area,
    'Price Per Marla': price_per_marla,
    'Block': block,
    'Phase': phase,
    'Sector': sector
}])

# Predict price
predicted_price = model.predict(new_property)
print(f"\nPredicted Price for your property: {predicted_price[0]:,.0f} PKR")
