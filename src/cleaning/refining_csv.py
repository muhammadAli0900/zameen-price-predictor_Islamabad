import pandas as pd

# Load your CSV
df = pd.read_csv("zameen_islamabad.csv")

# Helper functions
def convert_area_to_marla(area_text):
    try:
        if "Marla" in area_text:
            return float(area_text.split()[0])
        elif "Kanal" in area_text:
            return float(area_text.split()[0]) * 20
        else:
            return None  # Unknown unit
    except:
        return None

def convert_price(price):
    if isinstance(price, str):
        price = price.lower().replace(",", "").strip()
        if "crore" in price:
            return float(price.split()[0]) * 10000000
        elif "lakh" in price:
            return float(price.split()[0]) * 100000
    return None

# Apply conversions
df["Area (Marla)"] = df["Area"].apply(convert_area_to_marla)
df["Price (PKR)"] = df["Price"].apply(convert_price)

# Drop rows with missing data
df.dropna(subset=["Area (Marla)", "Price (PKR)"], inplace=True)

# Add price per Marla column
df["Price Per Marla"] = df["Price (PKR)"] / df["Area (Marla)"]
#Dropping price and area columns as they are no longer needed
df.drop(columns=["Price", "Area"], inplace=True)

# Save cleaned version
df.to_csv("zameen_islamabad_cleaned.csv", index=False)
print("✅ Cleaned data saved to 'zameen_islamabad_cleaned.csv'")

print("\n📊 Sample of Cleaned Data:")
print(df[["Title", "Location", "Beds", "Baths", "Area (Marla)", "Price (PKR)", "Price Per Marla"]].head(10).to_string(index=False))
