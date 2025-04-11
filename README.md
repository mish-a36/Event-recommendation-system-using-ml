# Personalised Event-recommendation-system-using-ml
Event recommender for students from college events ongoing accroding to the user interest as received as ratings feedback for an event.

This platform allows institutions to post events and users to receive personalized recommendations based on their behavior, such as clicks, ratings, and recency of interactions.

## 🚀 Features

- 🔐 Admin and User Login system
- 🏫 Multi-institution support
- 📅 Dynamic event posting and management
- 🤖 Machine Learning-based event recommendations using K-Nearest Neighbors (KNN)
- 🧠 Personalized suggestions based on:
  - User ratings (explicit feedback)
  - Clicks (implicit feedback)
  - Recency of interaction
- 📊 Admin analytics (future enhancement)
- 🖥️ Streamlit frontend for user dashboard
- 🧩 RESTful Flask API for ML integration
- 🗃️ MySQL database hosted on XAMPP server (localhost)

## 🛠️ Tech Stack

- **Frontend**: HTML/CSS, Streamlit
- **Backend**: PHP, Flask (for ML API)
- **Database**: MySQL (XAMPP)
- **Machine Learning**: Python, scikit-learn (KNN)
- **Server**: XAMPP (Apache + MySQL)

## 🧪 ML Recommendation System

The KNN model recommends top 5 events for each user by analyzing:
- Event category
- User ratings
- Clicked status
- Recency score (time-weighted interaction)

The model is trained  with `train_model.py` and served through `app.py`.
Python streamlit is used to build the frontend easily wuth less use of html/css for styling.




