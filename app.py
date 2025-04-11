import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import mysql.connector
import joblib
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- Database Configuration ---
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "event_recommendation_system"
}

@app.route("/recommend", methods=["GET"])
def recommend_events():
    user_id = request.args.get("user_id", type=int)
    if user_id is None:
        return jsonify({"error": "User ID is required"}), 400

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # --- Load trained model ---
        knn, label_encoder, scaler = joblib.load("models/knn_model2.pkl")

        # --- Fetch user interaction history ---
        cursor.execute("""
            SELECT e.category, ui.rating, ui.created_at
            FROM user_interest ui
            JOIN events e ON ui.event_id = e.id
            WHERE ui.user_id = %s
        """, (user_id,))
        user_history = pd.DataFrame(cursor.fetchall())

        if user_history.empty:
            return jsonify({"recommendations": []})  # No recommendations if no history

        user_history["created_at"] = pd.to_datetime(user_history["created_at"])
        user_history["recency_score"] = 1 / (1 + (pd.Timestamp.now() - user_history["created_at"]).dt.total_seconds())
        user_history["weight"] = user_history["rating"] * user_history["recency_score"]
        user_history["category_encoded"] = label_encoder.transform(user_history["category"].fillna("Others"))
        user_history["scaled_weight"] = scaler.transform(user_history[["weight"]])

        user_vectors = user_history[["category_encoded", "scaled_weight"]].values
        user_vector_mean = np.mean(user_vectors, axis=0).reshape(1, -1)

        # --- Fetch candidate events ---
        cursor.execute("""
            SELECT e.id, e.title, e.category, e.date
            FROM events e
            WHERE e.date >= CURDATE()
              AND e.id NOT IN (SELECT event_id FROM user_interest WHERE user_id = %s)
        """, (user_id,))
        candidates = pd.DataFrame(cursor.fetchall())

        if candidates.empty:
            return jsonify({"recommendations": []})

        candidates["category_encoded"] = label_encoder.transform(candidates["category"].fillna("Others"))
        candidates["recency_score"] = 1 / (1 + (pd.Timestamp.now() - pd.to_datetime(candidates["date"])).dt.total_seconds())
        candidates["weight"] = candidates["recency_score"] * 3
        candidates["scaled_weight"] = scaler.transform(candidates[["weight"]])
        candidate_vectors = candidates[["category_encoded", "scaled_weight"]].values

        if len(candidate_vectors) == 0:
            return jsonify({"recommendations": []})

        distances, indices = knn.kneighbors(candidate_vectors, n_neighbors=1)
        scores = distances.flatten()
        candidates["score"] = scores

        # Sort by similarity score (lower distance = more similar)
        recommended_events = candidates.sort_values("score").head(5)

        print(f"\n✅ Recommended Events for User {user_id}")
        print(recommended_events)

        # ✅ Rename and format output to match frontend expectations
        final_recommendations = recommended_events.drop(
            columns=["category_encoded", "recency_score", "weight", "scaled_weight", "score"]
        ).rename(columns={
            "id": "event_id",
            "title": "event_title",
            "category": "event_category"
        })

        return jsonify({"recommendations": final_recommendations.to_dict(orient="records")})

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"error": str(e)})

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    app.run(debug=True)


