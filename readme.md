# Islamabad Property Price Predictor

A machine learning project that predicts residential property prices in Islamabad using data scraped directly from Zameen.com. The entire pipeline is built from scratch — scraping, cleaning, training, and prediction — with no pre-made dataset involved.

![Python](https://img.shields.io/badge/Python-3.12-blue) ![Scikit-learn](https://img.shields.io/badge/Model-Random%20Forest-orange) ![Selenium](https://img.shields.io/badge/Scraper-Selenium-brightgreen)

---

## Why this project

Real estate data for Pakistani cities is not openly available in a usable format. Instead of downloading a ready-made dataset, I built a Selenium scraper to collect 1,000+ property listings from Zameen.com myself, then cleaned, structured, and modeled the data end to end. That process — not just the model — is what this project is about.

---

## Overview

| | |
|---|---|
| **Target variable** | Property Price (PKR) |
| **City** | Islamabad |
| **Listings collected** | 1,012 |
| **Model** | Random Forest Regressor |
| **R²** | 0.8472 |
| **RMSE** | 51,165,250 PKR |
| **MAE** | 24,188,613 PKR |

---

## Pipeline

**1. Scraping (src/scraper/zameen_scraper.py)**

Built with Selenium and ChromeDriver. Handles lazy-loaded listings, gracefully saves progress on manual stop (Ctrl+C), and skips listings with missing fields. Stores raw output to data/raw/.

Scraping Zameen.com was not straightforward. The site uses dynamic rendering, and getting the CSS selectors right took debugging time. ChromeDriver version had to be matched manually to the installed Chrome version before the scraper would even start.

**2. Cleaning (src/data_cleaning/clean_data.py)**

- Converted price strings like "4.5 Crore" to numeric PKR values
- Standardized area units (Kanal, Marla) into a single Marla column
- Added Price Per Marla as a derived feature
- Split vague location strings into Area, Block, Phase, Sector
- Removed duplicates and rows with invalid prices or areas

Final cleaned file: data/cleaned/zameen_islamabad_model_ready.csv

**3. Training (src/training_prediction_model.py)**

Features used: Beds, Baths, Area (Marla), Block, Phase, Sector

Full scikit-learn Pipeline:
- Numeric: SimpleImputer (median)
- Categorical: SimpleImputer (most frequent) + OneHotEncoder
- Model: RandomForestRegressor

The preprocessor and model are saved together as a single pipeline (models/best_model.pkl) so training, evaluation, and prediction always use identical transformations.

**4. Evaluation (src/evalute_model.py)**

Loads the saved pipeline, runs predictions on the cleaned dataset, prints MAE/RMSE/R², and saves actuals vs predicted to data/processed/predictions.csv.

**5. Prediction CLI (src/predict_price.py)**

Interactive script for getting a price estimate. Enter Area (Marla), Beds, Baths, and Sector. Block and Phase are filled from sector-level historical averages if not provided.

```
Enter Size (in Marla): 10
Enter Number of Bedrooms: 3
Enter Number of Bathrooms: 2
Enter Sector: F-10

Predicted Price: 12,500,000 PKR
```

---

## Model Results

| Model | R² | RMSE (PKR) | MAE (PKR) |
|---|---|---|---|
| Random Forest | 0.8472 | 51,165,250 | 24,188,613 |

R� of 0.84 on real estate data is solid. Property prices are inherently noisy — same sector, same size, different price depending on floor, view, renovation status, and factors the listing never mentions.

---

## How to Run

```bash
git clone https://github.com/muhammadAli0900/zameen-price-predictor_Islamabad.git
cd zameen-price-predictor_Islamabad
pip install -r requirements.txt
```

From the src/ folder:

```bash
# Train the model
python training_prediction_model.py

# Evaluate on cleaned data
python evalute_model.py

# Get a price prediction
python predict_price.py
```

---

## Project Structure

```
zameen-price-predictor_Islamabad/
├── data/
│   └── cleaned/
│       └── zameen_islamabad_model_ready.csv
├── models/
│   └── best_model.pkl
├── src/
│   ├── scraper/
│   │   └── zameen_scraper.py
│   ├── data_cleaning/
│   │   └── clean_data.py
│   ├── training_prediction_model.py
│   ├── evalute_model.py
│   └── predict_price.py
├── requirements.txt
└── .gitignore
```

---

## Future Plans

- Streamlit web app so anyone can get a price estimate without running the CLI
- Expand scraping to Lahore and Karachi for a multi-city model
- Add more granular location features to improve accuracy

---

## Disclaimer

Predictions are based on historical scraped data and do not reflect real-time market prices.

---

**Muhammad Ali** — BS Software Engineering, Sukkur IBA University  
[GitHub](https://github.com/muhammadAli0900)
