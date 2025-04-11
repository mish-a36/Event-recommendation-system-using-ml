import streamlit as st
import requests
import re  # For detecting URLs
from urllib.parse import quote

# Get event_id from query parameters
query_params = st.query_params
event_id = query_params.get("event_id")
institution_id = query_params.get("institution_id", "")
institution_name = query_params.get("institution_name", "")
user_name = query_params.get("user_name", "")
user_role = query_params.get("user_role", "")
admin_id = query_params.get("admin_id", "")


st.title("📅 Event Details")

if event_id:
    api_url = f"http://localhost/event_recommendation/backend/get_event_description.php?event_id={event_id}"
    response = requests.get(api_url)

    if response.status_code == 200:
        try:
            event_data = response.json()

            if event_data.get("status") == "success":
                # Display event title and date (if available)
                st.subheader(f"📌 Event: {event_data.get('title', 'Unknown Title')}")
                st.write(f"📅 Date: {event_data.get('date', 'No Date Provided')}")

                # Get description_extra

                description_extra = event_data.get("description_extra", "")
                description_extra = description_extra.strip() if description_extra is not None else ""


                if description_extra:
                    # Detect if it contains a valid URL
                    url_pattern = r"https?://[^\s]+"  # Regex for detecting URLs
                    match = re.search(url_pattern, description_extra)

                    if match:
                        # If URL exists, create a hyperlink
                        st.write("🔗 Click below for more details:")
                        st.markdown(f"[Registration link]({match.group()})", unsafe_allow_html=True)
                    else:
                        # If no URL, display plain text
                        st.write(f"ℹ️ {description_extra}")
                else:
                    st.warning("⚠️ No additional description provided.")

            else:
                st.error(f"❌ Error: {event_data.get('message', 'Unknown error occurred')}")

        except requests.exceptions.JSONDecodeError:
            st.error("❌ Error: Invalid JSON response from server.")

    else:
        st.error("⚠️ Failed to fetch event details. Please try again later.")

else:
    st.warning("⚠️ No event selected. Please provide a valid event ID.")

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