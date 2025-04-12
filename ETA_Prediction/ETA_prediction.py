import pandas as pd
import numpy as np
import joblib
from datetime import datetime

# --- Load Trained Model and Label Encoder ---
model = joblib.load("eta_predictor_model.pkl")
le_day = joblib.load("le_day.pkl")

# --- Load Excel Dataset ---
df = pd.read_excel(r"Excell_File_Directory")        #Excell_File_Directory

# --- Get Manual User Input ---
home_lat = float(input("Enter home latitude: "))
home_long = float(input("Enter home longitude: "))
office_lat = float(input("Enter office latitude: "))
office_long = float(input("Enter office longitude: "))
day_of_week = input("Enter day of week (e.g., Monday): ").capitalize()
time_leaving = input("Enter time of leaving (HH:MM): ")

# --- Extract Features ---
hour = int(time_leaving.split(":")[0])
day_encoded = le_day.transform([day_of_week])[0]
is_weekend = 1 if day_of_week in ['Saturday', 'Sunday'] else 0

# --- Match Similar Rides from Excel ---
tolerance = 0.01
df['hour'] = pd.to_datetime(df['departure_time'], format='%H:%M:%S').dt.hour

matched_rides = df[
    (abs(df['home_lat'] - home_lat) <= tolerance) &
    (abs(df['home_long'] - home_long) <= tolerance) &
    (abs(df['office_lat'] - office_lat) <= tolerance) &
    (abs(df['office_long'] - office_long) <= tolerance) &
    (df['day_of_week'].str.lower() == day_of_week.lower()) &
    (abs(df['hour'] - hour) <= 1)
]

# --- Predict ETA ---
if not matched_rides.empty:
    avg_distance = matched_rides['distance_km'].median()
    avg_traffic = matched_rides['traffic_level_percent'].median()
    fallback_eta = matched_rides['ETA_minutes'].median()

    input_features = pd.DataFrame([{
        'distance_km': avg_distance,
        'hour': hour,
        'day_of_week': day_encoded,
        'is_weekend': is_weekend,
        'traffic_level_percent': avg_traffic
    }])

    predicted_eta = model.predict(input_features)[0]
    print(f"\n✅ Predicted ETA (Model): {predicted_eta:.2f} minutes")
    print(f"🕒 Fallback ETA from historical data: {fallback_eta:.2f} minutes")

else:
    print("\n⚠️ No similar rides found in Excel.")
    print("❌ Unable to predict ETA with confidence.")
