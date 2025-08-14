import pandas as pd

# Load cleaned data
df_main = pd.read_csv("zameen_islamabad_cleaned.csv")
df_location = pd.read_csv("location_cleaned.csv")

# Remove duplicates from location data
df_location = df_location.drop_duplicates(subset=["Location"])

# Merge on 'Location' column
df_merged = pd.merge(df_main, df_location, on="Location", how="left")

# Keep only the required columns in your specified order
final_columns = [
    "Title", 
    "Price (PKR)", 
    "Beds", 
    "Baths", 
    "Area (Marla)", 
    "Price Per Marla", 
    "Area", 
    "Block", 
    "Phase", 
    "Sector"
]
df_final = df_merged[final_columns]

# Save final merged file
df_final.to_csv("zameen_islamabad_model_ready.csv", index=False)

print("✅ Final modeling-ready data saved to 'zameen_islamabad_model_ready.csv'")
print("\n📊 Sample preview:")
print(df_final.head(10).to_string(index=False))
