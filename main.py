import streamlit as st
from authentication import login_signup
from homepage import homepage
from profile import profile_page

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="CheckMate - AI Cheque Extractor",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state for authentication and navigation
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "dashboard"

# Check authentication status
if not st.session_state["authenticated"]:
    # Render login/signup functionality
    login_signup()
else:
    # Render page based on current_page state
    if st.session_state["current_page"] == "profile":
        profile_page()
    else:
        homepage()
