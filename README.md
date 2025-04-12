# 🚗 04TheInvincibles — ETA Prediction System

A smart travel-time prediction app developed during **QuantumHack25**. This system estimates commute time from **Home to Office** with **accuracy**,
using machine learning, live traffic data (non-Google), and simulated travel data.

---

## 📌 Assumptions

1. Data covers **3 months** of daily trips for **50 customers**.
2. Each customer has **random (lat, long)** for Home and Office.
3. **Google Maps API is not used**. Alternative API (like **TomTom**) is used.
4. ETA depends on **day of the week**, **time of day**, and **live traffic**.
5. Traffic is treated as **constant**. Accidents, roadblocks, and jams are ignored.

---

## 🔍 Features

- 🧪 Simulated ride data using Excel
- 📍 Random geolocation generation
- 🧠 ML model trained on time, day, and traffic conditions
- 🌐 Web app interface to input route and receive ETA
- 📊 High prediction accuracy (>95%)

---

## 🛠 Tech Stack

- **Python**, **Pandas**, **Scikit-learn**
- **HTML / CSS / JavaScript**
- **Live Traffic API**: (e.g., **TomTom**)

---

