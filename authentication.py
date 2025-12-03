import streamlit as st
import pymongo
import bcrypt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://pawardarshan1204_db_user:e8YWNKRO8G7W7Nf3@cluster0.zr2canz.mongodb.net/")

client = pymongo.MongoClient(MONGO_URI)
db = client['infosys']
users_collection = db['users']

# Register user
def register_user(username, password):
    # Check if user already exists
    existing_user = users_collection.find_one({"username": username})
    if existing_user:
        st.error("User already exists. Please login.")
        return False
    
    # Hash the password before storing
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users_collection.insert_one({"username": username, "password": hashed_password.decode()})
    
    # Show success notification with balloons
    st.success("✅ Signup successful! Welcome aboard!")
    st.balloons()
    
    # Set session state to mark the user as authenticated
    st.session_state["authenticated"] = True
    st.session_state["username"] = username
    st.toast(f"🎉 Welcome {username}! Setting up your account...", icon="✨")
    import time
    time.sleep(1)
    st.rerun()  # Trigger rerun to refresh the session state
    return True

# Authenticate user
def authenticate_user(username, password):
    # Check if the user exists
    user = users_collection.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user["password"].encode()):
        return True  # Successful authentication
    return False  # Invalid credentials

# Login / Signup Page
def login_signup():
    # Split-screen authentication design inspired by reference
    st.markdown("""
    <style>
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-15px); }
        }
        
        @keyframes slideInLeft {
            from { opacity: 0; transform: translateX(-100px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        @keyframes slideInRight {
            from { opacity: 0; transform: translateX(100px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        /* Hide default streamlit elements */
        [data-testid="stToolbar"] { display: none; }
        header { display: none; }
        
        /* Remove default container margins */
        .main .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
        
        /* Container for columns */
        [data-testid="column"] {
            padding: 0 !important;
            height: 100vh;
        }
        
        /* Right column styling - acts as auth-right */
        [data-testid="column"]:last-child {
            background: white !important;
            background-color: #FFFFFF !important;
            display: flex !important;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            animation: slideInRight 0.8s ease;
            overflow-y: auto;
        }
        
        [data-testid="column"]:last-child > div {
            width: 100%;
            max-width: 450px;
            padding: 2rem 1rem;
        }
        
        [data-testid="column"]:last-child::-webkit-scrollbar {
            width: 8px;
        }
        
        [data-testid="column"]:last-child::-webkit-scrollbar-track {
            background: #F5F5F5;
        }
        
        [data-testid="column"]:last-child::-webkit-scrollbar-thumb {
            background: #1a1a2e;
            border-radius: 4px;
        }
        
        [data-testid="column"]:last-child [data-testid="stVerticalBlock"] {
            gap: 0 !important;
        }
        
        [data-testid="stVerticalBlock"] {
            gap: 0 !important;
        }
        
        [data-testid="stHorizontalBlock"] {
            gap: 0 !important;
        }
        
        /* Left side - Illustration */
        .auth-left {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 3rem;
            animation: slideInLeft 0.8s ease;
            position: relative;
            overflow: hidden;
            min-height: 100vh;
            height: 100vh;
        }
        
        .auth-left::before {
            content: '';
            position: absolute;
            width: 600px;
            height: 600px;
            background: radial-gradient(circle, rgba(220, 53, 69, 0.15) 0%, transparent 70%);
            top: -200px;
            left: -200px;
            animation: float 8s ease-in-out infinite;
        }
        
        .illustration-container {
            max-width: 450px;
            width: 100%;
            text-align: center;
            position: relative;
            z-index: 1;
            animation: float 6s ease-in-out infinite;
        }
        
        .illustration-icon {
            font-size: 15rem;
            line-height: 1;
            margin-bottom: 2rem;
            filter: drop-shadow(0 20px 40px rgba(220, 53, 69, 0.3));
        }
        
        .illustration-title {
            font-size: 2.5rem;
            font-weight: 800;
            color: #FFFFFF;
            margin-bottom: 1rem;
            letter-spacing: 0.5px;
        }
        
        .illustration-subtitle {
            font-size: 1rem;
            color: rgba(255, 255, 255, 0.85);
            font-weight: 400;
            line-height: 1.8;
            max-width: 400px;
        }
        
        /* Right side - Form */
        .auth-right {
            width: 100%;
        }
        
        .auth-right > div > div {
            width: 100%;
            max-width: 450px;
            margin: 0 auto;
        }
        
        .form-header {
            margin-bottom: 2rem;
            animation: fadeIn 1s ease 0.3s both;
            text-align: center;
        }
        
        .welcome-text {
            font-size: 1.1rem;
            color: #666;
            font-weight: 500;
            margin-bottom: 0.5rem;
        }
        
        .form-title {
            font-size: 2.5rem;
            font-weight: 800;
            color: #1a1a2e;
            margin-bottom: 0.5rem;
        }
        
        .form-divider {
            display: flex;
            align-items: center;
            margin: 1rem 0;
        }
        
        .form-divider::before,
        .form-divider::after {
            content: '';
            flex: 1;
            height: 1px;
            background: #E0E0E0;
        }
        
        .form-divider-text {
            padding: 0 1rem;
            color: #999;
            font-size: 0.9rem;
            font-weight: 600;
        }
        
        /* Social button styling */
        .social-btn {
            background: white;
            border: 1px solid #E0E0E0;
            border-radius: 50px;
            padding: 0.75rem 1.5rem;
            margin: 0.5rem 0;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.75rem;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
            color: #333;
        }
        
        .social-btn:hover {
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            transform: translateY(-1px);
        }
        
        .social-icon {
            font-size: 1.2rem;
        }
        
        /* Custom input styling */
        [data-testid="column"]:last-child .stTextInput > div > div > input {
            border: 2px solid #E8E8E8 !important;
            border-radius: 12px !important;
            padding: 0.9rem 1rem !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            background: #FAFAFA !important;
        }
        
        [data-testid="column"]:last-child .stTextInput > div > div > input:focus {
            border-color: #1a1a2e !important;
            box-shadow: 0 0 0 2px rgba(26, 26, 46, 0.1) !important;
            background: white !important;
        }
        
        [data-testid="column"]:last-child .stTextInput {
            width: 100%;
        }
        
        .input-label {
            font-size: 0.9rem;
            font-weight: 600;
            color: #555;
            margin-bottom: 0.4rem;
            margin-top: 0.8rem;
            display: block;
        }
        
        .input-icon {
            font-size: 1rem;
            margin-right: 0.3rem;
        }
        
        /* Button styling */
        [data-testid="column"]:last-child .stButton > button {
            background: #D3D3D3 !important;
            color: #666 !important;
            padding: 0.9rem 2rem !important;
            border-radius: 50px !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            border: none !important;
            box-shadow: none !important;
            transition: all 0.3s ease !important;
            text-transform: none;
            letter-spacing: 0.5px;
            width: 100%;
        }
        
        [data-testid="column"]:last-child .stButton > button:hover {
            background: #C0C0C0 !important;
            transform: translateY(-1px) !important;
        }
        
        [data-testid="column"]:last-child .stButton {
            width: 100%;
        }
        
        /* Radio button styling */
        [data-testid="column"]:last-child .stRadio > div {
            display: flex !important;
            justify-content: center !important;
            gap: 1rem !important;
            background: transparent !important;
            padding: 0 !important;
            margin-bottom: 1.5rem !important;
        }
        
        [data-testid="column"]:last-child .stRadio > div > label {
            background: #F5F5F5 !important;
            padding: 0.75rem 2rem !important;
            border-radius: 50px !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            color: #666 !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            border: 2px solid transparent !important;
        }
        
        [data-testid="column"]:last-child .stRadio > div > label:has(input:checked) {
            background: #1a1a2e !important;
            color: white !important;
            box-shadow: 0 2px 10px rgba(26, 26, 46, 0.3) !important;
            transform: translateY(-2px);
        }
        
        [data-testid="column"]:last-child .stRadio {
            width: 100%;
        }
        
        /* Checkbox styling */
        [data-testid="column"]:last-child .stCheckbox {
            width: 100%;
        }
        
        /* Alert/message styling */
        [data-testid="column"]:last-child .stAlert,
        [data-testid="column"]:last-child .stSuccess,
        [data-testid="column"]:last-child .stError,
        [data-testid="column"]:last-child .stWarning {
            width: 100%;
            margin: 0.5rem 0;
        }
        
        .remember-forgot {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 1rem 0;
            font-size: 0.9rem;
        }
        
        .forgot-link {
            color: #1a1a2e;
            font-weight: 600;
            text-decoration: underline;
            cursor: pointer;
        }
        
        .register-prompt {
            text-align: center;
            margin-top: 1.5rem;
            margin-bottom: 0;
            font-size: 0.95rem;
            color: #666;
        }
        
        .register-link {
            color: #1a1a2e;
            font-weight: 700;
            cursor: pointer;
            text-decoration: underline;
            transition: color 0.3s ease;
        }
        
        .register-link:hover {
            color: #000;
        }
        
        @media (max-width: 968px) {
            [data-testid="column"]:first-child {
                display: none;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Split-screen layout with proper positioning
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.markdown("""
        <div class="auth-left">
            <div class="illustration-container">
                <div class="illustration-icon">🏦</div>
                <div class="illustration-title">Design with us</div>
                <div class="illustration-subtitle">
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi lobortis maximus nunc, ac rhoncus odio congue quis. Sed ac semper orci, eu porttitor lacus.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_right:
        # Form header
        st.markdown("""
        <div class="form-header">
            <div class="form-title">Sign in</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Social login buttons
        st.markdown("""
        <div class="social-btn">
            <span class="social-icon">🔵</span>
            <span>Continue with Google</span>
        </div>
        <div class="social-btn">
            <span class="social-icon">🐦</span>
            <span>Continue with Twitter</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="form-divider"><span class="form-divider-text">OR</span></div>', unsafe_allow_html=True)
        
        # Tab selection
        choice = st.radio(
            "",
            ["🔐 Login", "✨ Sign Up"],
            key="login_signup_radio",
            horizontal=True,
            label_visibility="collapsed"
        )
        
        # Email input
        st.markdown('<div class="input-label">User name or email address</div>', unsafe_allow_html=True)
        username = st.text_input(
            "Email",
            key="username_input",
            placeholder="",
            label_visibility="collapsed"
        )
        
        # Password input  
        st.markdown('<div class="input-label">Your password</div>', unsafe_allow_html=True)
        password = st.text_input(
            "Password",
            type="password",
            key="password_input",
            placeholder="",
            label_visibility="collapsed"
        )
    
        if choice == "✨ Sign Up":
            if st.button("Sign up", key="signup_button", use_container_width=True):
                if username and password:
                    if len(password) < 6:
                        st.error("❌ Password must be at least 6 characters long!")
                        st.toast("Password too short", icon="⚠️")
                    else:
                        register_user(username, password)
                else:
                    st.warning("⚠️ Please fill in all fields")
                    st.toast("Missing credentials", icon="📝")
                    
            st.markdown("""
            <div class="register-prompt">
                Already have an account? 
                <a href="#" class="register-link">Sign in</a>
            </div>
            """, unsafe_allow_html=True)
            
        else:  # Login
            # Remember me and forgot password
            col_a, col_b = st.columns(2)
            with col_a:
                remember = st.checkbox("Remember me", key="remember_me")
            with col_b:
                st.markdown('<div style="text-align: right;"><a href="#" class="forgot-link">Forgot Password?</a></div>', unsafe_allow_html=True)
            
            if st.button("Sign in", key="login_button", use_container_width=True):
                if username and password:
                    if authenticate_user(username, password):
                        st.success(f"✅ Welcome back!")
                        st.toast(f"🎉 Login successful!", icon="🔓")
                        st.session_state["authenticated"] = True
                        st.session_state["username"] = username
                        import time
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials")
                        st.toast("🔒 Authentication failed", icon="⚠️")
                else:
                    st.warning("⚠️ Please fill in all fields")
                    st.toast("Missing credentials", icon="📝")
                    
            st.markdown("""
            <div class="register-prompt">
                Don't have an account? 
                <a href="#" class="register-link">Sign up</a>
            </div>
            """, unsafe_allow_html=True)
