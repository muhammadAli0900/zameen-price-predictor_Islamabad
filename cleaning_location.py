import pandas as pd
import re

# Load your CSV (with original Location column)
df = pd.read_csv("zameen_islamabad_cleaned.csv")  # adjust filename if needed

def parse_location(location):
    if pd.isna(location):
        return pd.Series({"Area": None, "Block": None, "Phase": None, "Sector": None})

    loc = location.strip()
    area = block = phase = sector = None

    parts = [p.strip() for p in loc.split(",")]

    sector_match = re.search(r'\b[A-Z]-\d+(/\d+)?\b', loc)
    if sector_match:
        sector = sector_match.group(0)

    if " - " in loc:
        dash_parts = [p.strip() for p in loc.split(" - ")]
        area = dash_parts[0]
        if len(dash_parts) > 1:
            block_or_phase = dash_parts[1]
            if "Block" in block_or_phase:
                block = block_or_phase
            elif "Phase" in block_or_phase:
                phase = block_or_phase
    else:
        if len(parts) >= 1:
            first_part = parts[0]
            if not sector:
                area = first_part
            else:
                if len(parts) > 1:
                    area = parts[1]
                else:
                    area = None

    if area:
        area = area.replace("Islamabad", "").strip()
        if area == "":
            area = None

    return pd.Series({"Area": area, "Block": block, "Phase": phase, "Sector": sector})

# Apply parsing only on Location column
location_parsed = df["Location"].apply(parse_location)

# Combine original Location with parsed columns
location_df = pd.concat([df["Location"], location_parsed], axis=1)

# Save to a new CSV just for location details
location_df.to_csv("location_cleaned.csv", index=False)

print("✅ Location data parsed and saved separately to 'zameen_islamabad_location_cleaned.csv'")
print(location_df.head(10).to_string(index=False))
