import streamlit as st
import requests
import json

query_params = st.query_params
institution_id = query_params.get("institution_id")
institution_name = query_params.get("institution_name")

st.subheader("🔐 Login")
email_login = st.text_input("Enter your email")
password_login = st.text_input("Enter your password", type="password")

if st.button("Login"):
    if email_login and password_login:
        login_data = {"email": email_login, "password": password_login}
        response = requests.post("http://localhost/event_recommendation/backend/login.php", json=login_data)

        if response.status_code == 200:
            try:
                user_data = response.json()
                if user_data["status"] == "success":
                    st.success(f"✅ Welcome back, {user_data['user']['name']}!")

                    # ✅ Redirect using query parameters (Passing user details)
                    redirect_url = f"http://localhost:8501/welcome?institution_id={institution_id}&institution_name={institution_name}&user_name={user_data['user']['name']}&user_role={user_data['user']['role']}&admin_id={user_data['user']['id']}"

                    st.markdown(f'<meta http-equiv="refresh" content="0; URL={redirect_url}">', unsafe_allow_html=True)

                else:
                    st.error(f"❌ {user_data['message']}")
            except json.JSONDecodeError:
                st.error("❌ Error: Unable to parse server response.")
        else:
            st.error("❌ Server error. Try again later.")
    else:
        st.warning("⚠️ Please enter both email and password.")


