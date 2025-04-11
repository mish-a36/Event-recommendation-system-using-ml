import streamlit as st
import requests
from datetime import datetime
from urllib.parse import quote

st.set_page_config(page_title="Recommended Events", layout="centered")

st.title("🎯 Recommended Events for You")

# Extract query parameters
query_params = st.query_params
event_id = query_params.get("event_id")
institution_id = query_params.get("institution_id", "")
institution_name = query_params.get("institution_name", "")
user_name = query_params.get("user_name", "")
user_role = query_params.get("user_role", "")
admin_id = query_params.get("admin_id", "")

# Validate and extract user/institution ID
try:
    user_id = int(query_params.get("user_id", "0"))
    institution_id = int(query_params.get("institution_id", "0"))
except (ValueError, TypeError):
    st.error("❌ Invalid or missing `user_id` or `institution_id` in query parameters.")
    st.stop()

# Call recommendation backend
recommend_api = f"http://127.0.0.1:5000/recommend?user_id={user_id}"
recommend_response = requests.get(recommend_api)

try:
    data = recommend_response.json()

    # If backend returns a list instead of {"recommendations": [...]}, adjust here:
    recommended_events = data if isinstance(data, list) else data.get("recommendations", [])

    today_date = datetime.today().date()
    upcoming_events = []

    for event in recommended_events:
        event_id = event.get("event_id") or event.get("id")  # Support both keys
        if not event_id:
            continue

        # Fetch event date via fetch_event_date.php (optional if already present)
        date_api = f"http://localhost/event_recommendation/backend/fetch_event_date.php?event_id={event_id}"
        date_response = requests.get(date_api)

        try:
            date_data = date_response.json()
            event_date_str = date_data.get("date")
            if not event_date_str:
                continue

            event_date = datetime.strptime(event_date_str, "%Y-%m-%d").date()

            if event_date >= today_date:
                event["date"] = event_date_str
                upcoming_events.append(event)

        except Exception as e:
            st.warning(f"⚠️ Failed to process event ID {event_id}: {e}")

    # 🔍 Debug: Check the structure of upcoming events
    # st.write("🔍 Debug: Upcoming Events List", upcoming_events)

    if upcoming_events:
        for event in upcoming_events:
            with st.container():
                st.markdown(f"""
                <div style="background-color: #f0f2f6; border-radius: 12px; padding: 15px; border-left: 6px solid #007bff;">
                    <h4 style="color: #007bff;">🎉 {event.get('event_title') or event.get('title')}</h4>
                    <p style="color: black;"><b>Category:</b> {event.get('event_category') or event.get('category')}</p>
                    <p style="color: black;"><b>Conducted On:</b> {event.get('date')}</p>
                </div>""", unsafe_allow_html=True)
    else:
        st.warning("📭 No upcoming events found in recommendations.")

except Exception as e:
    st.error(f"❌ Error parsing API response: {e}")

back_url = (
    f"http://localhost:8501/welcome"
    f"?institution_id={quote(str(institution_id))}"
    f"&institution_name={quote(institution_name)}"
    f"&user_name={quote(user_name)}"
    f"&user_role={quote(user_role)}"
    f"&admin_id={quote(str(admin_id))}"
)
if st.button("🔙 Go Back"):
    st.markdown(f'<meta http-equiv="refresh" content="0;URL={back_url}">', unsafe_allow_html=True)
