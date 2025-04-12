from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import joblib

app = Flask(__name__)

# Load trained model and label encoder
model = joblib.load("eta_predictor_model.pkl")
le_day = joblib.load("le_day.pkl")

# Load ride data from Excel
df = pd.read_excel("ride_data_with_traffic_eta.xlsx")
df['hour'] = pd.to_datetime(df['departure_time'], format='%H:%M:%S').dt.hour

@app.route("/", methods=["GET", "POST"])
def index():
    eta_result = None
    warning = None

    if request.method == "POST":
        try:
            # Get form input
            home_lat = float(request.form["home_lat"])
            home_long = float(request.form["home_long"])
            office_lat = float(request.form["office_lat"])
            office_long = float(request.form["office_long"])
            day_of_week = request.form["day_of_week"].capitalize()
            time_leaving = request.form["time_leaving"]
            
            hour = int(time_leaving.split(":")[0])
            day_encoded = le_day.transform([day_of_week])[0]
            is_weekend = 1 if day_of_week in ['Saturday', 'Sunday'] else 0

            # Match similar rides
            tolerance = 0.01
            matched_rides = df[
                (abs(df['home_lat'] - home_lat) <= tolerance) &
                (abs(df['home_long'] - home_long) <= tolerance) &
                (abs(df['office_lat'] - office_lat) <= tolerance) &
                (abs(df['office_long'] - office_long) <= tolerance) &
                (df['day_of_week'].str.lower() == day_of_week.lower()) &
                (abs(df['hour'] - hour) <= 1)
            ]

            if not matched_rides.empty:
                avg_distance = matched_rides['distance_km'].median()
                avg_traffic = matched_rides['traffic_level_percent'].median()

                input_features = pd.DataFrame([{
                    'distance_km': avg_distance,
                    'hour': hour,
                    'day_of_week': day_encoded,
                    'is_weekend': is_weekend,
                    'traffic_level_percent': avg_traffic
                }])

                predicted_eta = model.predict(input_features)[0]
                eta_result = round(predicted_eta, 2)

            else:
                warning = "⚠️ No similar rides found in the data. Unable to confidently predict ETA."

        except Exception as e:
            warning = f"❌ Error: {e}"

    return render_template("index.html", eta_result=eta_result, warning=warning)

if __name__ == "__main__":
    app.run(debug=True)
