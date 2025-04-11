import streamlit as st
import requests

st.set_page_config(page_title="Institution Home", layout="wide")

st.title("🏫 Select Your Institution")

# ✅ Fetch institutions from the backend
def fetch_institutions():
    try:
        response = requests.get("http://localhost/event_recommendation/backend/list_institutions.php")  # Adjust API endpoint
        if response.status_code == 200:
            return response.json().get("institutions", [])
        return []
    except requests.exceptions.RequestException:
        st.error("Error fetching institutions.")
        return []

institutions = fetch_institutions()

if not institutions:
    st.warning("No institutions found. Please register a new one.")
else:
    st.write("Click on an institution to visit its dashboard:")
    
    for inst in institutions:
        if st.button(inst["institution_name"], key=inst["id"]):
            # ✅ Store institution details in query params
            st.query_params["institution_id"] = str(inst["id"])
            st.query_params["institution_name"] = inst["institution_name"]
            st.query_params["page"] = "institution_dashboard"
            st.rerun()  # ✅ Refresh for redirection

# ✅ Redirect if query params contain 'institution_dashboard'
query_params = st.query_params
if query_params.get("page") == "institution_dashboard" and "institution_id" in query_params:
    institution_name = query_params["institution_name"]
    
    st.write(f"Redirecting to {institution_name}'s Dashboard...")  # ✅ Show institution name

    # ✅ Redirect using meta refresh with institution ID & Name in URL
    redirect_url = f'http://localhost:8501/login?institution_id={query_params["institution_id"]}&institution_name={institution_name}'
    st.markdown(f'<meta http-equiv="refresh" content="0; URL={redirect_url}">', unsafe_allow_html=True)
