from cheque_extractor import cheque_extractor_app
import streamlit as st

def homepage():
    st.title("Welcome to Checkmate: Automated Cheque Data Extractor!")
    
    # Render the cheque extractor app
    cheque_extractor_app()
    
    # Add a logout button
    if st.button("Logout", key="logout_button"):
        st.session_state["authenticated"] = False  # Set authentication state to False
        st.rerun()  # Rerun the app to redirect to login/signup page
