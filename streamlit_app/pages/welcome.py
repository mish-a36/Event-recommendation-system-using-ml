import streamlit as st
import requests
import json
import webbrowser
import random
from datetime import date
from datetime import datetime
from urllib.parse import quote
st.set_page_config(page_title="Welcome", layout="wide")

# ✅ Retrieve and store session state values
query_params = st.query_params
st.session_state["institution_id"] = query_params.get("institution_id", st.session_state.get("institution_id"))
st.session_state["institution_name"] = query_params.get("institution_name", st.session_state.get("institution_name"))
st.session_state["user_name"] = query_params.get("user_name", st.session_state.get("user_name"))
st.session_state["user_role"] = query_params.get("user_role", st.session_state.get("user_role"))
st.session_state["user_id"] = query_params.get("admin_id", st.session_state.get("user_id"))

# ✅ Check if user is logged in
if not st.session_state.get("user_name"):
    st.error("⚠️ You must log in first!")
    st.stop()

st.header(f"🎉 Welcome back, {st.session_state['user_name']}!")

EVENTS_API_URL = "http://localhost/event_recommendation/backend/get_events.php"



# ✅ Fetch events function
def fetch_events(institution_id):
    try:
        response = requests.get(f"{EVENTS_API_URL}?institution_id={institution_id}")
        return response.json().get("events", []) if response.status_code == 200 else []
    except requests.exceptions.RequestException:
        st.error("Error fetching events.")
        return []
def fetch_event_rating(user_id, event_id):
    API_GET_RATING = "http://localhost/event_recommendation/backend/get_ratings.php"
    response = requests.get(f"{API_GET_RATING}?user_id={user_id}&event_id={event_id}")
    if response.status_code == 200:
        try:
            data = response.json()
            if "rating" in data and data["rating"] is not None:
                return int(data["rating"]) 
            else:
                return None
        except json.JSONDecodeError:
            return None
    return None
def fetch_recommendations(user_id):
    try:
        url = f"http://localhost:5000/recommend?user_id={user_id}"
        response = requests.get(url)
        if response.status_code == 200:
            st.write("📦 Raw response:", response.json())  # Debug output
            return response.json()
        else:
            st.warning(f"❗ Backend returned status {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Failed to fetch recommendations: {e}")
        return []

# ✅ Submit rating function
def submit_rating(event_id, event_title, event_description, event_date, rating):
    payload = {
        "user_id": st.session_state["user_id"],
        "user_name": st.session_state["user_name"],
        "event_id": event_id,
        "event_title": event_title,
        "event_description": event_description,
        "event_date": event_date,
        "rating": rating
    }
    response = requests.post("http://localhost/event_recommendation/backend/submit_rating.php",
                             data=json.dumps(payload), headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        try:
            result = response.json()
            st.success("✅ Rating submitted successfully!" if result.get("status") == "success" else f"❌ Error: {result.get('message')}")
        except json.JSONDecodeError:
            st.error("❌ Failed to parse server response.")
    else:
        st.error("❌ Server error. Try again later.")

st.header("📅 All Upcoming Events")

institution_id = st.session_state.get("institution_id")
events = fetch_events(institution_id)


if st.session_state["user_role"] == "student":
    
    if not events:
        st.warning("🚀 No events posted yet. Stay tuned!")
    else:
        today_date = datetime.today().date()
        upcoming_events = [event for event in events if datetime.strptime(event["date"], "%Y-%m-%d").date() >= today_date]

        for event in upcoming_events:
            with st.container():
                st.markdown(f"""
                <div style="background-color: #f0f2f6; border-radius: 12px; padding: 15px; border-left: 6px solid #007bff;">
                    <h4 style="color: #007bff;">🎉 {event['title']}</h4>
                    <p style="color: black;"><b>Description:</b> {event['description']}</p>
                    <p style="color: black;"><b>Conducted On:</b> {event['date']}</p>
                </div>""", unsafe_allow_html=True)

                query_params = st.query_params
                user_id = query_params.get("admin_id")
                institution_id = query_params.get("institution_id")
                institution_name = query_params.get("institution_name")
                user_name = query_params.get("user_name")
                user_role = query_params.get("user_role")
                admin_id = query_params.get("admin_id")
                event_id = event["id"]
                details_url = (f"http://localhost:8501/event_details"f"?event_id={quote(str(event_id))}"f"&institution_id={quote(str(institution_id))}"f"&institution_name={quote(institution_name)}"f"&user_name={quote(user_name)}"f"&user_role={quote(user_role)}"f"&admin_id={quote(str(admin_id))}")

                if st.button("🔍 Click to know more and to register", key=f"register_{event['id']}"):
                    if event_id and user_id:
                        log_data = {"event_id": event_id, "user_id": user_id}
                        response = requests.post("http://localhost/event_recommendation/backend/log_event_click.php", json=log_data)
                        if response.status_code == 200:
                            st.success("Click logged successfully!")
                        else:
                            st.error("⚠️ Failed to log click!")
                    webbrowser.open_new_tab(details_url)

                # Rating system
                saved_rating = fetch_event_rating(user_id, event["id"])
                if saved_rating is not None:
                    st.write(f"⭐ This event is currently rated: {saved_rating}")
                else:
                    st.write("Rate this event for recommendations.")

                rating = st.radio("Select a rating:", [1, 2, 3, 4, 5], horizontal=True, key=f"rating_{event['id']}")
                if st.button("Submit Rating", key=f"submit_rating_{event['id']}"):
                    submit_rating(event['id'], event['title'], event['description'], event['date'], rating)

        # Recommendations Section
        # Extract user_id from URL query parameters 
        query_params = st.query_params
        admin_id = query_params.get("admin_id")  # used as user_id
        institution_id = query_params.get("institution_id")
        institution_name = query_params.get("institution_name")
        user_name = query_params.get("user_name")
        user_role = query_params.get("user_role")

        # Validate required parameters
        if not admin_id or not institution_id:
            st.error("❌ Missing 'admin_id' or 'institution_id' in URL.")
            st.stop()

        # Build the recommendations URL
        recommendations_url = (
            f"http://localhost:8501/recommendations"
            f"?user_id={quote(str(admin_id))}"
            f"&institution_id={quote(str(institution_id))}"
            f"&institution_name={quote(institution_name)}"
            f"&user_name={quote(user_name)}"
            f"&user_role={quote(user_role)}"
            f"&admin_id={quote(str(admin_id))}"
        )

        # Button to open recommendations
        if st.button("🎯 Show Recommendations", key=f"recommend_button_{admin_id}"):
            webbrowser.open_new_tab(recommendations_url)
elif st.session_state["user_role"] == "admin":
    query_params = st.query_params
    selected_event_id = query_params.get("selected_event_id", [None])[0]
    update_clicked = query_params.get("clicked", ["false"])[0] == "true"
    if not events:
        st.warning("🚀 No events posted yet. Stay tuned!")
    else:
        today_date = datetime.today().date()
        upcoming_events = [event for event in events if datetime.strptime(event["date"], "%Y-%m-%d").date() >= today_date]
        for event in upcoming_events:
            with st.expander(f"🔹 {event['title']} ({event['date']})"):
                st.write(f"**Description:** {event['description']}")
                if st.button(f"✏️ Edit {event['title']}", key=f"edit_{event['id']}"):
                    # Set the selected event in query parameters
                    st.query_params["selected_event_id"] = event["id"]

    # Check if an event is selected for editing
    if selected_event_id:
        # Fetch the selected event
        selected_event = next((e for e in events if str(e["id"]) == selected_event_id), None)

        if selected_event:
            st.subheader(f"✏️ Edit Event: {selected_event['title']}")
            with st.form("edit_event_form"):
                new_title = st.text_input("New Event Title", value=selected_event["title"])
                new_description = st.text_area("New Event Description", value=selected_event["description"])
                new_date = st.date_input("New Event Date", value=date.fromisoformat(selected_event["date"]))
                update_submit = st.form_submit_button("Update Event")

                if update_submit:
                    # Set query parameter to track update click
                    st.query_params["selected_event_id"] = selected_event["id"]
                    st.query_params["clicked"]="true"

        # If update button is clicked, execute the update request
        if query_params.get("clicked") == "true":
            event_data = {
                "event_id": selected_event_id,
                "title": new_title.strip(),
                "description": new_description.strip(),
                "date": str(new_date),
                "institution_id": institution_id,
                "admin_id": st.session_state["user_id"]
            }
            response = requests.post("http://localhost/event_recommendation/backend/update_event.php", data=json.dumps(event_data),
                                     headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                st.success("✅ Event updated successfully!")
            else:
                st.error("❌ Update failed.")

            # Reset query parameters after update
            st.query_params["selected_event_id"] = " "
            st.query_params["clicked"]="false"


    st.subheader("📅 Add New Event")
    with st.form("event_form"):
        title = st.text_input("Event Title")
        description = st.text_area("Event Description (Optional)")
        event_date = st.date_input("Event Date")
        more_description = st.text_area("Attach the registration link , or elaborative information about the event")
        categories = ["Sports", "Hackathon", "Technical Event", "Others"]
        category = st.selectbox("Select Event Category", categories) 
        submit = st.form_submit_button("Add Event")
        
        if submit and title and event_date:
            event_data = {
                "title": title.strip(),
                "description": description.strip() if description else "",
                "description_extra": more_description.strip() if more_description else "",
                "date": str(event_date),
                "institution_id": institution_id,
                "admin_id": st.session_state["user_id"],
                "category": category  
            }
            response = requests.post("http://localhost/event_recommendation/backend/add_event.php",
                                     data=json.dumps(event_data), headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                st.success("✅ Event added successfully!")
            else:
                st.error("❌ Failed to add event.")

    st.subheader("🆕 Register a New Student")
    with st.form("user_auth"):
        name = st.text_input("👤 Username")
        email = st.text_input("📧 Email")
        password = st.text_input("🔑 Password", type="password")
        submit = st.form_submit_button("Register")
        if submit and name and email and password:
            register_data = {"name": name, "email": email, "password": password, "institution_id": institution_id, "role": "student"}
            response = requests.post("http://localhost/event_recommendation/backend/register_user.php",
                                     data=json.dumps(register_data), headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                st.success("✅ User registered successfully!")
            else:
                st.error("❌ Registration failed.")

if st.button("Logout"):
    st.session_state.clear()
    st.markdown('<meta http-equiv="refresh" content="0; URL=http://localhost:8501/institution_home">', unsafe_allow_html=True)

