import streamlit as st
import bcrypt

# Initialize session-based user storage (no database required)
def init_users_db():
    if 'users_db' not in st.session_state:
        # Pre-hashed passwords for default users
        st.session_state['users_db'] = {
            'admin': bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode(),
            'test': bcrypt.hashpw('test123'.encode('utf-8'), bcrypt.gensalt()).decode()
        }

# Register user
def register_user(username, password):
    init_users_db()
    
    # Check if user already exists
    if username in st.session_state['users_db']:
        st.error("❌ User already exists. Please login.")
        return False
    
    # Hash the password before storing
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    st.session_state['users_db'][username] = hashed_password.decode()
    st.success("✅ Signup successful!")

    # Set session state to mark the user as authenticated
    st.session_state["authenticated"] = True
    st.session_state["username"] = username
    st.rerun()
    return True

# Authenticate user
def authenticate_user(username, password):
    init_users_db()
    
    # Check if the user exists
    if username in st.session_state['users_db']:
        stored_password = st.session_state['users_db'][username]
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode()):
            return True
    return False

# Login / Signup Page
def login_signup():
    init_users_db()
    
    # Center the card using columns
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Card container with custom styling
        st.markdown("""
            <style>
                .login-card {
                    background: white;
                    padding: 2rem;
                    border-radius: 15px;
                    border: 2px solid #e0e0e0;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    margin-top: 3rem;
                }
            </style>
        """, unsafe_allow_html=True)
        
        # Card header
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center;'>🔐 Welcome to CheckMate</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: gray;'>AI-Powered Cheque Data Extractor</h3>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # User selects login or signup
        choice = st.radio("Select an option:", ["Login", "Signup"], horizontal=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # User input fields
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")

        if choice == "Signup":
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")
            if st.button("Sign Up", type="primary", use_container_width=True):
                if username and password and confirm_password:
                    if password != confirm_password:
                        st.error("❌ Passwords don't match!")
                    elif len(password) < 6:
                        st.error("❌ Password must be at least 6 characters!")
                    else:
                        register_user(username, password)
                else:
                    st.warning("⚠️ Please fill in all fields.")
        else:  # Login functionality
            if st.button("Login", type="primary", use_container_width=True):
                if username and password:
                    if authenticate_user(username, password):
                        st.session_state["authenticated"] = True
                        st.session_state["username"] = username
                        st.success(f"✅ Welcome back, {username}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password.")
                else:
                    st.warning("⚠️ Please enter a username and password.")
        
        # Show default credentials hint
        if choice == "Login":
            st.markdown("<br>", unsafe_allow_html=True)
            st.info("💡 Default credentials: **admin** / **admin123** or **test** / **test123**")
        
        st.markdown('</div>', unsafe_allow_html=True)
