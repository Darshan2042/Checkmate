import streamlit as st
import bcrypt

# Pre-hashed passwords for better performance (only hash once at startup)
PREHASHED_USERS = {
    'admin': '$2b$12$KIXxFQqKhHvXxPZc3yN0xOYW5fZQJz8Yh0x4sL6vL9nqFQxR3g5SK',  # admin123
    'test': '$2b$12$8YqZ9yHxQJ3l7HxPZc3yN0xOYW5fZQJz8Yh0x4sL6vL9nqFQxR3g5SK'   # test123
}

# Initialize session state for users database
def init_users_db():
    if 'users_db' not in st.session_state:
        st.session_state['users_db'] = PREHASHED_USERS.copy()

# Register user
def register_user(username, password):
    init_users_db()  # Ensure users_db is initialized
    # Check if user already exists
    if username in st.session_state['users_db']:
        st.error("❌ User already exists. Please login.")
        return False
    
    # Hash the password before storing
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    st.session_state['users_db'][username] = hashed_password.decode()
    
    # Show success notification
    st.success("✅ Account created successfully!")
    st.balloons()
    
    # Set session state to mark the user as authenticated
    st.session_state["authenticated"] = True
    st.session_state["username"] = username
    st.rerun()
    return True

# Authenticate user
def authenticate_user(username, password):
    init_users_db()  # Ensure users_db is initialized
    if username in st.session_state['users_db']:
        stored_password = st.session_state['users_db'][username]
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode()):
            return True
    return False

# Login / Signup Page
def login_signup():
    init_users_db()  # Ensure users_db is initialized
    st.markdown("""
    <style>
        /* Hide default streamlit elements */
        [data-testid="stToolbar"] { display: none; }
        header { display: none; }
        footer { display: none; }
        
        /* Clean gradient background */
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            background-attachment: fixed;
        }
        
        .main .block-container {
            padding: 2rem 1rem !important;
            max-width: 100% !important;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        
        /* Simple login card */
        .login-container {
            background: white;
            border-radius: 20px;
            padding: 3rem 2.5rem;
            width: 100%;
            max-width: 450px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }
        
        /* Title */
        .login-title {
            color: #333;
            font-size: 2rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        /* Input styling */
        .stTextInput > div > div > input {
            background: #f5f5f5 !important;
            border: 2px solid #e0e0e0 !important;
            border-radius: 10px !important;
            color: #333 !important;
            padding: 0.9rem 1rem !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
            background: white !important;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            padding: 0.9rem 2rem !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            font-size: 1.05rem !important;
            border: none !important;
            width: 100%;
            margin-top: 1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
        }
        
        /* Checkbox */
        .stCheckbox label {
            color: #666 !important;
            font-size: 0.95rem !important;
        }
        
        /* Links */
        .link-text {
            color: #667eea;
            text-align: center;
            margin-top: 1.5rem;
            font-size: 0.95rem;
            cursor: pointer;
        }
        
        .link-text:hover {
            text-decoration: underline;
        }
        
        /* Hide labels */
        .stTextInput label { display: none !important; }
        
        /* Alerts */
        .stSuccess, .stError, .stWarning {
            border-radius: 10px !important;
            margin: 1rem 0 !important;
        }
        
        [data-testid="stVerticalBlock"] { gap: 0.5rem !important; }
    </style>
    """, unsafe_allow_html=True)
    
    # Center container
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # Title
    st.markdown('<h1 class="login-title">Welcome Back</h1>', unsafe_allow_html=True)
    
    # Tab for Login/Signup
    tab = st.radio("", ["Login", "Sign Up"], horizontal=True, label_visibility="collapsed")
    
    if tab == "Login":
        # Login Form
        st.markdown("---")
        username = st.text_input("Username", placeholder="Enter your username", key="login_username")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
        
        col1, col2 = st.columns(2)
        with col1:
            remember = st.checkbox("Remember me")
        
        if st.button("Login", key="login_btn"):
            if username and password:
                if authenticate_user(username, password):
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = username
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
            else:
                st.warning("⚠️ Please enter both username and password")
        
        st.markdown('<p class="link-text">Default: admin/admin123 or test/test123</p>', unsafe_allow_html=True)
    
    else:
        # Signup Form
        st.markdown("---")
        new_username = st.text_input("Username", placeholder="Choose a username", key="signup_username")
        new_password = st.text_input("Password", type="password", placeholder="Choose a password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password", key="confirm_password")
        
        if st.button("Create Account", key="signup_btn"):
            if new_username and new_password and confirm_password:
                if new_password != confirm_password:
                    st.error("❌ Passwords don't match")
                elif len(new_password) < 6:
                    st.error("❌ Password must be at least 6 characters")
                else:
                    register_user(new_username, new_password)
            else:
                st.warning("⚠️ Please fill in all fields")
    
    st.markdown('</div>', unsafe_allow_html=True)
