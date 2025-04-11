import streamlit as st
import requests
import json

API_URL = "http://localhost/event_recommendation/backend/register_institution.php"

st.title("Register Your Institution")

with st.form("register_institution_form"):
    institution_name = st.text_input("Institution Name")
    admin_name = st.text_input("Admin Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    location = st.text_input("Location")

    submit_button = st.form_submit_button("Register Institution")

if submit_button:
    if not institution_name or not admin_name or not email or not password or not location:
        st.error("⚠️ All fields are required!")
    else:
        data = {
            "institution_name": institution_name.strip(),
            "name": admin_name.strip(),
            "email": email.strip(),
            "password": password.strip(),
            "location": location.strip()
        }

        headers = {'Content-Type': 'application/json'}

        # 🚀 Make sure to send data as JSON
        response = requests.post(API_URL, data=json.dumps(data), headers=headers)  

        try:
            result = response.json()
          

            if response.status_code == 200 and result["status"] == "success":
                st.success(result["message"])
            else:
                st.error(f"❌ {result.get('message', 'Registration failed!')}")
        except requests.exceptions.JSONDecodeError:
            st.error("This institution already exists")
