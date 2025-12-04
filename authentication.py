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
    
    # Page background image (uses public URL; replace if needed)
    background_url = "PIC.jpg"
    st.markdown(f"""
        <style>
            /* Full-page background image */
            .stApp {{
                background-image: url('{background_url}');
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            /* Optional subtle overlay for readability */
            .stApp::before {{
                content: "";
                position: fixed;
                inset: 0;
                background: rgba(255, 255, 255, 0.35);
                pointer-events: none;
                z-index: 0;
            }}
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize view state: 'login' or 'register'
    if 'auth_view' not in st.session_state:
        st.session_state['auth_view'] = 'login'

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
                .card-footer {
                    margin-top: 1rem;
                    text-align: center;
                    color: #666;
                }
            </style>
        """, unsafe_allow_html=True)

        # Card wrapper
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center;'>🔐 Welcome to CheckMate</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: gray;'>AI-Powered Cheque Data Extractor</h3>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Render based on view
        if st.session_state['auth_view'] == 'login':
            # Helper text inside the card
            st.markdown("<p style='text-align:center; color:#555;'>Please login to access CheckMate and start extracting cheque data.</p>", unsafe_allow_html=True)
            # Login inputs
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")

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

            # # Default credentials hint
            # st.markdown("<br>", unsafe_allow_html=True)
            # st.info("💡 Default credentials: **admin** / **admin123** or **test** / **test123**")

            # Footer: Register link/button
            st.markdown("<div class='card-footer'>Don't have an account?</div>", unsafe_allow_html=True)
            if st.button("Register", use_container_width=True):
                st.session_state['auth_view'] = 'register'
                st.rerun()

        else:
            # Register inputs
            username = st.text_input("Username", placeholder="Choose a username")
            password = st.text_input("Password", type="password", placeholder="Choose a password")
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

            # Footer: Back to login
            if st.button("Back to Login", use_container_width=True):
                st.session_state['auth_view'] = 'login'
                st.rerun()

        # Close card wrapper
        st.markdown('</div>', unsafe_allow_html=True)
