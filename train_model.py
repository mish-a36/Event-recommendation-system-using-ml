# ---------------- train_model.py ----------------
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import mysql.connector
import joblib
import os

# --- Database Configuration ---
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "event_recommendation_system"
}

# --- Connect to Database ---
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor(dictionary=True)

# --- Fetch interaction data ---
cursor.execute("""
    SELECT ui.user_id, ui.event_id, ui.rating, ui.created_at, e.category
    FROM user_interest ui
    JOIN events e ON ui.event_id = e.id
""")
data = pd.DataFrame(cursor.fetchall())

if data.empty:
    print("No interaction data found.")
    exit()

# --- Feature Engineering ---
data["created_at"] = pd.to_datetime(data["created_at"])
data["recency_score"] = 1 / (1 + (pd.Timestamp.now() - data["created_at"]).dt.total_seconds())
data["weight"] = data["rating"] * data["recency_score"]

label_encoder = LabelEncoder()
data["category_encoded"] = label_encoder.fit_transform(data["category"].fillna("Others"))

scaler = MinMaxScaler()
data["scaled_weight"] = scaler.fit_transform(data[["weight"]])

features = data[["category_encoded", "scaled_weight"]].values

# --- Train KNN Model ---
knn = NearestNeighbors(n_neighbors=5, metric="euclidean")
knn.fit(features)

# --- Save Model ---
os.makedirs("models", exist_ok=True)
print("Saving model to:", os.path.abspath("../models/knn_model2.pkl"))
joblib.dump((knn, label_encoder, scaler), "../models/knn_model2.pkl")

print("Model trained and saved successfully.")

cursor.close()
connection.close()

