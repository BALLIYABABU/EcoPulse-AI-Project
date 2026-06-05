import os
import json
import pandas as pd
import numpy as np
import xgboost as xgb
import shap

def generate_dataset():
    np.random.seed(42)
    
    # 365 days from June 6, 2025 to June 5, 2026 (T+0)
    dates = pd.date_range(start="2025-06-06", end="2026-06-05")
    n_days = len(dates)
    
    # Generate weather variables (seasonal patterns for Bengaluru)
    # Bengaluru weather: Cool dry winter (Dec-Feb), Hot dry summer (Mar-May), Monsoon (Jun-Sep), Post-monsoon (Oct-Nov)
    day_of_year = dates.dayofyear.to_numpy()
    
    # Temperature (mean around 24°C, seasonal variation)
    temp = 24.0 + 5.0 * np.sin(2 * np.pi * (day_of_year - 100) / 365.0) + np.random.normal(0, 1.5, n_days)
    
    # Humidity (higher in monsoon, lower in summer)
    humidity = 65.0 + 20.0 * np.sin(2 * np.pi * (day_of_year - 200) / 365.0) + np.random.normal(0, 5.0, n_days)
    humidity = np.clip(humidity, 20.0, 95.0)
    
    # Rainfall (mainly June to September)
    rainfall = np.zeros(n_days)
    monsoon_days = (dates.month >= 6) & (dates.month <= 9)
    rainfall[monsoon_days] = np.random.exponential(8.0, sum(monsoon_days)) * (np.random.rand(sum(monsoon_days)) > 0.4)
    non_monsoon_days = ~monsoon_days
    rainfall[non_monsoon_days] = np.random.exponential(2.0, sum(non_monsoon_days)) * (np.random.rand(sum(non_monsoon_days)) > 0.8)
    
    # Wind speed (m/s) (higher in monsoon, lower in winter/calm days)
    wind_speed = 3.0 + 1.5 * np.sin(2 * np.pi * (day_of_year - 150) / 365.0) + np.random.normal(0, 0.6, n_days)
    wind_speed = np.clip(wind_speed, 0.5, 8.0)
    
    # Human activity variables
    # Industrial activity index (0 to 1, weekly cycle)
    industrial_emissions = 0.65 + 0.15 * np.sin(2 * np.pi * (day_of_year) / 365.0) + np.random.normal(0, 0.05, n_days)
    # Weekend drop in industrial activity
    is_sunday = np.array([d.weekday() == 6 for d in dates])
    industrial_emissions[is_sunday] *= 0.7
    industrial_emissions = np.clip(industrial_emissions, 0.2, 0.95)
    
    # Traffic density (0 to 1, weekly cycle)
    traffic_density = 0.7 + 0.1 * np.cos(2 * np.pi * (day_of_year) / 180.0) + np.random.normal(0, 0.04, n_days)
    # Weekday vs Weekend traffic
    is_weekend = np.array([d.weekday() in (5, 6) for d in dates])
    traffic_density[is_weekend] *= 0.8
    traffic_density = np.clip(traffic_density, 0.3, 0.95)
    
    # Green cover (slow decay over time due to urbanization, starting around 0.20 down to 0.12)
    vegetation_index = 0.20 - 0.08 * (np.arange(n_days) / n_days) + np.random.normal(0, 0.005, n_days)
    vegetation_index = np.clip(vegetation_index, 0.05, 0.3)
    
    # Base AQI and pollutant calculations based on emission, traffic, weather
    # AQI ranges in India: 0-50 Good, 51-100 Satisfactory, 101-200 Moderate, 201-300 Poor, 301-400 Very Poor, 401+ Severe
    # We want a base equation that responds logically:
    # High emissions & traffic -> High AQI
    # High wind speed -> lower AQI (dispersion)
    # Rainfall -> lower AQI (washout)
    # Low green cover -> higher AQI (less absorption)
    
    base_aqi = 60.0
    aqi = (
        base_aqi +
        industrial_emissions * 130.0 +
        traffic_density * 90.0 -
        wind_speed * 12.0 -
        rainfall * 0.4 -
        vegetation_index * 120.0 +
        np.random.normal(0, 10.0, n_days)
    )
    
    # Make sure today (June 5, 2026) matches the primary demo story conditions exactly:
    # AQI: 168, Industrial: 0.74, Traffic: 0.82, Wind: 1.2, Green: 12% (vegetation_index=0.12)
    # Let's override the last row (today)
    aqi[-1] = 168.0
    industrial_emissions[-1] = 0.74
    traffic_density[-1] = 0.82
    wind_speed[-1] = 1.2
    vegetation_index[-1] = 0.12
    temp[-1] = 28.5
    humidity[-1] = 55.0
    rainfall[-1] = 0.0
    
    # Also create pollutants based on AQI (roughly proportional)
    pm25 = aqi * 0.55 + np.random.normal(0, 3, n_days)
    pm10 = aqi * 1.3 + np.random.normal(0, 8, n_days)
    no2 = aqi * 0.3 + industrial_emissions * 20.0 + np.random.normal(0, 2, n_days)
    so2 = aqi * 0.08 + industrial_emissions * 10.0 + np.random.normal(0, 1, n_days)
    co = aqi * 0.01 + traffic_density * 0.8 + np.random.normal(0, 0.1, n_days)
    o3 = aqi * 0.25 - temp * 0.2 + np.random.normal(0, 3, n_days)
    
    # Clip to realistic environmental limits
    pm25 = np.clip(pm25, 5.0, 450.0)
    pm10 = np.clip(pm10, 10.0, 600.0)
    no2 = np.clip(no2, 2.0, 150.0)
    so2 = np.clip(so2, 1.0, 80.0)
    co = np.clip(co, 0.1, 8.0)
    o3 = np.clip(o3, 2.0, 200.0)
    aqi = np.clip(aqi, 10.0, 500.0)
    
    # Day features
    df = pd.DataFrame({
        "date": dates.strftime("%Y-%m-%d"),
        "pm25": np.round(pm25, 1),
        "pm10": np.round(pm10, 1),
        "no2": np.round(no2, 1),
        "so2": np.round(so2, 1),
        "co": np.round(co, 2),
        "o3": np.round(o3, 1),
        "temperature": np.round(temp, 1),
        "humidity": np.round(humidity, 1),
        "wind_speed": np.round(wind_speed, 2),
        "rainfall": np.round(rainfall, 1),
        "industrial_emissions": np.round(industrial_emissions, 2),
        "traffic_density": np.round(traffic_density, 2),
        "vegetation_index": np.round(vegetation_index, 2),
        "aqi": np.round(aqi, 0).astype(int)
    })
    
    # Create lag and rolling features
    df["aqi_lag_1"] = df["aqi"].shift(1)
    df["aqi_lag_7"] = df["aqi"].shift(7)
    df["aqi_roll_7"] = df["aqi"].shift(1).rolling(window=7).mean()
    
    # Fill NaN from shift with forward/backward fill
    df["aqi_lag_1"] = df["aqi_lag_1"].bfill()
    df["aqi_lag_7"] = df["aqi_lag_7"].bfill()
    df["aqi_roll_7"] = df["aqi_roll_7"].bfill()
    
    df["day_of_week"] = dates.weekday
    df["month"] = dates.month
    df["is_holiday"] = 0
    # Add a few Indian holidays for feature engineering
    holiday_months = [8, 10, 1, 11] # Aug, Oct, Jan, Nov
    holiday_days = [15, 2, 26, 12] # Independence, Gandhi, Republic, Diwali-ish
    for m, d in zip(holiday_months, holiday_days):
        df.loc[(df["month"] == m) & (pd.to_datetime(df["date"]).dt.day == d), "is_holiday"] = 1
        
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/bengaluru_aqi_12months.csv", index=False)
    print("CSV created successfully.")
    
    # Train model to generate xgboost_model.json and SHAP values sample
    train_and_save_model(df)

def train_and_save_model(df):
    # Features to use for forecasting
    feature_cols = [
        "temperature", "humidity", "wind_speed", "rainfall",
        "industrial_emissions", "traffic_density", "vegetation_index",
        "aqi_lag_1", "aqi_lag_7", "aqi_roll_7",
        "day_of_week", "month", "is_holiday"
    ]
    
    X = df[feature_cols]
    y = df["aqi"]
    
    # Train XGBoost
    model = xgb.XGBRegressor(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.08,
        random_state=42
    )
    model.fit(X, y)
    
    # Save model
    model.save_model("data/xgboost_model.json")
    print("XGBoost model saved.")
    
    # Calculate SHAP values for the current state (last row in df)
    explainer = shap.TreeExplainer(model)
    # Run explainer on the last row
    last_row = X.iloc[[-1]]
    shap_values = explainer(last_row)
    
    # Format SHAP data for frontend serialization
    # shap_values[0].values contains the SHAP impact value for each feature
    # shap_values[0].base_values is the average prediction baseline
    # last_row features contain the actual values
    shap_data = {
        "base_value": float(explainer.expected_value),
        "prediction": float(model.predict(last_row)[0]),
        "features": {}
    }
    
    for idx, name in enumerate(feature_cols):
        shap_val = float(shap_values.values[0][idx])
        feat_val = float(last_row[name].values[0])
        shap_data["features"][name] = {
            "shap_value": shap_val,
            "feature_value": feat_val
        }
        
    # Write to data/shap_values_sample.json
    with open("data/shap_values_sample.json", "w") as f:
        json.dump(shap_data, f, indent=2)
    print("SHAP values sample saved.")

if __name__ == "__main__":
    generate_dataset()
