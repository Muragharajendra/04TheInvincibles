import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score, mean_absolute_error
import xgboost as xgb

# --- Load Your Excel ---
df = pd.read_excel("C:\\Users\\murag\\OneDrive\\Captures - Copy\\Hackathon\\ride_data_with_traffic_eta.xlsx")


# --- Encode Day_of_Week ---
le_day = LabelEncoder()
df['day_of_week'] = le_day.fit_transform(df['day_of_week'])  # Monday=0, Sunday=6

# --- Define Features and Target ---
features = ['distance_km', 'departure_time', 'day_of_week', 'is_weekend', 'traffic_level_percent']
df['hour'] = pd.to_datetime(df['departure_time'], format='%H:%M:%S').dt.hour
X = df[['distance_km', 'hour', 'day_of_week', 'is_weekend', 'traffic_level_percent']]
y = df['ETA_minutes']

# --- Split and Train Model ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, max_depth=5, learning_rate=0.1)
model.fit(X_train, y_train)

# --- Evaluate (Optional) ---
y_pred = model.predict(X_test)
print(f"R²: {r2_score(y_test, y_pred):.4f}")
print(f"MAE: {mean_absolute_error(y_test, y_pred):.2f} minutes")

# --- Save Model and Encoder ---
joblib.dump(model, "eta_predictor_model.pkl")
joblib.dump(le_day, "le_day.pkl")

print("✅ Saved model as 'eta_predictor_model.pkl'")
print("✅ Saved label encoder as 'le_day.pkl'")
