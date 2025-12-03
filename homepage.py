from cheque_extractor import cheque_extractor_app
import streamlit as st

def homepage():
    # Header with user greeting
    username = st.session_state.get("username", "User")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"""
        <div style='animation: slideInLeft 0.8s ease;'>
            <h1>👋 Welcome back, {username}!</h1>
            <p style='font-size: 1.2rem; color: #2563EB; font-weight: 600;'>Ready to extract cheque data with AI magic? ✨</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🚪 Logout", key="logout_button"):
            st.toast("👋 Logging out... See you soon!", icon="🔒")
            st.session_state["authenticated"] = False
            import time
            time.sleep(1)
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Render the cheque extractor app
    cheque_extractor_app()
