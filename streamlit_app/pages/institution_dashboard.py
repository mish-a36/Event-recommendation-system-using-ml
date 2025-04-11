import streamlit as st
import requests
import json

st.set_page_config(page_title="Institution Dashboard", layout="wide")
st.title("\U0001F3EB Institution Dashboard")

# ✅ Retrieve institution ID and name from query params
query_params = st.query_params
institution_id = query_params.get("institution_id")
institution_name = query_params.get("institution_name")

if institution_name:
    st.markdown(f"## **Welcome to {institution_name}'s Page!**")
else:
    st.error("No institution selected. Please go back and select an institution.")
    if st.button("Go Back and Select an Institution"):
        st.query_params["page"] = "institution_home"
        st.markdown('<meta http-equiv="refresh" content="0; URL=http://localhost:8501/institution_home">', unsafe_allow_html=True)

# ✅ Display posted events (Fetched from backend)
st.write("### \U0001F4C5 Events Posted by Admin:")

EVENTS_API_URL = "http://localhost/event_recommendation/backend/get_events.php"

def fetch_events(institution_id):
    try:
        response = requests.get(f"{EVENTS_API_URL}?institution_id={institution_id}")
        if response.status_code == 200:
            return response.json().get("events", [])
        return []
    except requests.exceptions.RequestException:
        st.error("Error fetching events.")
        return []

if institution_id:
    events = fetch_events(institution_id)
    
    if not events:
        st.warning("🚀 No events posted yet. Stay tuned!")
 
    else:
        for event in events:
            with st.container():
                st.markdown(
                    f"""
                    <div style="
                        background-color: #f0f2f6; 
                        border-radius: 12px; 
                        padding: 15px; 
                        margin: 10px 0;
                        border-left: 6px solid #007bff;
                        width: 100%;
                    ">
                        <h4 style="color: #007bff; margin-bottom: 5px;">🎉 {event['title']}</h4>
                        <p style="margin: 5px 0; font-size: 20px; color: #333;">
                            📌 <b>Description:</b> {event['description']}
                        </p>
                        <p style="margin: 5px 0; font-size: 20px; color: #666;">
                            📅 <b>Conducted On: </b> <b>{event['date']}</b>
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        query_params["popup"] = "false"
        if st.button(f"📝 Register for {event['title']}", key=f"register_{event['id']}"):
            st.query_params["popup"] = "true"
        if query_params.get("popup") == "true":
            st.markdown("""
            <div style="background-color: blue; padding: 15px; border-radius: 10px; width: 50%;">
                <h4>Confirm Registration</h4>
                <p>Type 'confirm' below to complete your registration.</p>
            </div>
            """, unsafe_allow_html=True)

            user_input = st.text_input("Type 'confirm' to register:")

            if user_input.lower() == "confirm":
                st.success("✅ Successfully Registered!")
                st.query_params["popup"] = "false"
                st.rerun()
            elif user_input:
                st.error("❌ Incorrect input. Type 'confirm' exactly.")

        # # Streamlit button below event details
        # if st.button(f"🔍 View {event['title']}", key=event["id"]):
        #     st.query_params["event_id"] = str(event["id"])
        #     st.query_params["event_name"] = event["title"]
        #     st.query_params["page"] = "event_details"
        #     st.rerun()




# ✅ User Authentication Section
st.write("---")
st.write("## 🔑 User Authentication")

# 🔹 Login Section

# 🔹 Register Section (Role is fixed to 'student')

# ✅ Button to go back
if st.button("Back to Institution Home"):
    st.query_params["page"] = "institution_home"
    st.markdown('<meta http-equiv="refresh" content="0; URL=http://localhost:8501/institution_home">', unsafe_allow_html=True)

