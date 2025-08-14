# Islamabad Real Estate Price Predictor

This project predicts **real estate prices** in Islamabad based on property features like size, number of bedrooms, bathrooms, and sector. It uses **machine learning** trained on scraped data from Zameen.com.

---

## Features
- **Data Collection**: Automated web scraping using **Selenium** and **ChromeDriver**.
- **Data Cleaning**: Pandas-based preprocessing for structured datasets.
- **Model Training**: Machine learning regression model trained on historical property data.
- **Evaluation**: Metrics to assess model accuracy.
- **Price Prediction Tool**: CLI-based script where users can input property details to get estimated prices.

---

## Technologies Used
- **Python**
- **Pandas**
- **Scikit-learn**
- **Joblib**
- **Selenium**
- **ChromeDriver**

---

## Project Structure
```
.
├── data/cleaned/                      # Cleaned datasets
├── models/                            # Saved trained models
├── src/
│   ├── training_prediction_model.py   # Train & save the ML model
│   ├── evaluate_model.py               # Evaluate trained model performance
│   ├── predict_price.py                # Predict price for user input
│   ├── scrape_data.py                   # Web scraping from Zameen.com
│   ├── preprocess_data.py               # Clean & prepare scraped data
│
├── requirements.txt                    # Project dependencies
├── README.md                           # Project documentation
├── update.txt                          # Daily progress updates
├── whatisthis.txt                      # Full project explanation
```

---

## How to Run
### 1. Clone the repository
```bash
git clone https://github.com/muhammadAli0900/zameen-price-predictor_Islamabad.git
cd zameen-price-predictor_Islamabad
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run price prediction
```bash
python src/predict_price.py
```
Follow the prompts to input:
- Size (Marla)
- Number of Bedrooms
- Number of Bathrooms
- Sector

The program will return an estimated price.

---

## Example Prediction
```
Enter Size (in Marla): 10
Enter Number of Bedrooms: 3
Enter Number of Bathrooms: 2
Enter Sector: F-10

Predicted Price: 12,500,000 PKR
```

---

## Model Details
- **Algorithm**: RandomForestRegressor
- **Features Used**:
  - Beds
  - Baths
  - Area (Marla)
  - Price Per Marla
  - Block
  - Phase
  - Sector

---

## Disclaimer
Predictions are based on historical scraped data and may not reflect real-time market prices.