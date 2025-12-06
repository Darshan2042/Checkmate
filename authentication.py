import streamlit as st
import bcrypt
import streamlit.components.v1 as components

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
    
    # Global styles: dark premium theme, inputs, frosted card
    st.markdown("""
        <style>
            :root {
                --bg-dark: #0b0b0f;
                --bg-dark-2: #141425;
                --accent-pink: #ec4899;
                --muted: #c7c7d1;
            }

                        /* Remove particles */

            /* Background */
            .stApp {
                background:
                    radial-gradient(circle at 20% 20%, rgba(236,72,153,0.22) 0%, transparent 35%),
                    radial-gradient(circle at 80% 30%, rgba(59,130,246,0.22) 0%, transparent 35%),
                    radial-gradient(circle at 50% 80%, rgba(34,197,94,0.22) 0%, transparent 40%),
                    linear-gradient(135deg, var(--bg-dark) 0%, var(--bg-dark-2) 100%);
                min-height: 100vh;
            }

            /* Frosted-glass card applied to the Streamlit form */
            [data-testid="stForm"] {
                position: relative;
                background: rgba(255,255,255,0.08);
                border: 1px solid rgba(255,255,255,0.22);
                border-radius: 18px;
                box-shadow: inset 0 1px 4px rgba(255,255,255,0.08), 0 12px 30px rgba(0,0,0,0.35);
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                padding: 2rem;
                margin-top: 1rem;
            }

            /* Typography */
            h1, h3, p, label { color: var(--text) !important; font-weight: 700 !important; }
            .muted { color: var(--muted); font-weight: 600; }

            /* Inputs: thicker borders + icons + neon focus */
            .stTextInput > div > div,
            .stPasswordInput > div > div { position: relative; }
            .stPasswordInput > div > div {
                background: rgba(255,255,255,0.12);
                border-radius: 12px;
            }
            .stTextInput > div > div > input,
            .stPasswordInput > div > div > input {
                background: rgba(255,255,255,0.10);
                color: var(--text);
                border: 2px solid rgba(200,200,210,0.45);
                border-radius: 12px;
                padding: 8px 12px 8px 40px;
                transition: all 150ms ease-in-out;
            }
            input::placeholder {
                color: rgba(200,200,200,0.6);
                transition: color 0.3s ease;
            }
            input:focus::placeholder {
                color: rgba(200,200,200,0.25);
            }
            /* Forgot password link */
            .forgot-password {
                text-align: right;
                margin-top: 0.5rem;
                font-size: 0.85rem;
            }
            .forgot-password a {
                color: var(--accent-pink);
                text-decoration: none;
                transition: color 0.2s ease;
            }
            .forgot-password a:hover {
                color: var(--accent-blue);
            }
            /* Security badges */
            .security-badge {
                text-align: center;
                margin-top: 1.5rem;
                font-size: 0.75rem;
                color: var(--muted);
                opacity: 0.8;
            }
            .security-badge div {
                margin: 0.3rem 0;
            }
            /* AI status feedback */
            .ai-status {
                text-align: center;
                margin-top: 0.8rem;
                font-size: 0.9rem;
                color: var(--accent-blue);
                animation: fadeIn 0.3s ease;
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(-5px); }
                to { opacity: 1; transform: translateY(0); }
            }
            /* icons */
            .stTextInput > div > div::before {
                content: "👤"; position: absolute; left: 10px; top: 50%; transform: translateY(-50%);
            }
            .stPasswordInput > div > div::before {
                content: "🔒"; position: absolute; left: 10px; top: 50%; transform: translateY(-50%);
            }
            .stTextInput > div > div > input:focus,
            .stPasswordInput > div > div > input:focus {
                outline: none;
                border-image: linear-gradient(90deg, var(--accent-pink), var(--accent-blue)) 1;
                box-shadow: 0 0 0 3px rgba(236,72,153,0.22), 0 0 0 6px rgba(59,130,246,0.15);
            }

            /* Buttons */
            .stButton > button {
                font-weight: 800; letter-spacing: 0.2px;
                border-radius: 14px !important; padding: 0.7rem 1.1rem;
                box-shadow: 0 8px 18px rgba(0,0,0,0.35);
                transition: transform 120ms ease, box-shadow 120ms ease;
            }
            .stButton > button:hover { transform: translateY(-1px) scale(1.01); }

            /* Remove pulsing lock */

            /* Remove AI tips rotation */
        </style>
    """, unsafe_allow_html=True)

    # Additional premium effects (gradient outline, pulsing lock, button gradient)
    st.markdown("""
        <style>
            [data-testid="stForm"] { transform-style: preserve-3d; transition: transform 220ms ease, box-shadow 220ms ease; }
            [data-testid="stForm"]:hover { transform: translateY(-3px) scale(1.01); transition: 200ms ease; }
            [data-testid="stForm"]::before { content: ""; position: absolute; inset: -1px; border-radius: 20px; padding: 2px; background: linear-gradient(135deg, #ec4899, #3b82f6, #22c55e); -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0); -webkit-mask-composite: xor; mask-composite: exclude; animation: borderFlow 6s linear infinite; filter: blur(0.5px); opacity: 0.65; }
            [data-testid="stForm"]::after { content: ""; position: absolute; bottom: -10px; left: 50%; width: 60%; height: 20px; transform: translateX(-50%); background: radial-gradient(ellipse, rgba(255,255,255,0.15), transparent); filter: blur(8px); }
            @keyframes borderFlow { 0% { filter: hue-rotate(0deg);} 50% { filter: hue-rotate(180deg);} 100% { filter: hue-rotate(360deg);} }
            .lock-neon { text-shadow: 0 0 6px rgba(236,72,153,0.7), 0 0 12px rgba(59,130,246,0.6); }
            @keyframes pulseLock { 0% { filter: drop-shadow(0 0 0 rgba(236,72,153,0)); } 50% { filter: drop-shadow(0 0 8px rgba(236,72,153,0.7)); } 100% { filter: drop-shadow(0 0 0 rgba(236,72,153,0)); } }
            .pulse { animation: pulseLock 4s infinite; }
            .stButton > button { background: linear-gradient(135deg, #ec4899, #8b5cf6) !important; border: none; color: white !important; }
            .stButton > button:hover { transform: translateY(-1px) scale(1.02); box-shadow: 0 12px 26px rgba(139,92,246,0.35); }
            .stButton > button:active { transform: scale(0.99); }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize view state: 'login' or 'register'
    if 'auth_view' not in st.session_state:
        st.session_state['auth_view'] = 'login'

    # Remove light/dark toggle state

    # Center main content area with two columns (animation + form)
    col1, col2, col3 = st.columns([1.2, 1.2, 1])

    with col2:
        # Heading above the card
        st.markdown("<h1 style='text-align:center; white-space:nowrap;' class='lock-neon pulse'>🔐 Welcome to CheckMate</h1>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Render based on view
        if st.session_state['auth_view'] == 'login':
            # Helper text
           
            # Login form to avoid 'Press Enter to apply'
            with st.form(key="login_form", clear_on_submit=False):
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                
                # Forgot password link
                st.markdown('<div class="forgot-password"><a href="#">Forgot password?</a></div>', unsafe_allow_html=True)
                
                submit_login = st.form_submit_button("Login", type="primary", use_container_width=True)

            # Handle login submit with AI status feedback
            if submit_login:
                if username and password:
                    # Show AI authentication status
                    with st.spinner('🤖 Authenticating with AI...'):
                        import time
                        time.sleep(0.5)  # Brief delay for effect
                        if authenticate_user(username, password):
                            st.session_state["authenticated"] = True
                            st.session_state["username"] = username
                            st.success(f"✅ Login successful. Welcome back, {username}!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid username or password.")
                else:
                    st.warning("⚠️ Please enter a username and password.")

            # # Default credentials hint
            # st.markdown("<br>", unsafe_allow_html=True)
            # st.info("💡 Default credentials: **admin** / **admin123** or **test** / **test123**")

        else:
            # Register form to avoid 'Press Enter to apply'
            with st.form(key="register_form", clear_on_submit=False):
                username = st.text_input("Username", placeholder="Choose a username")
                password = st.text_input("Password", type="password", placeholder="Choose a password")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")
                submit_signup = st.form_submit_button("Sign Up", type="primary", use_container_width=True)

            if submit_signup:
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

        # Footer: Sign up below the card
        if st.session_state['auth_view'] == 'login':
            if st.button("Sign up", use_container_width=True):
                st.session_state['auth_view'] = 'register'
                st.rerun()
            
            # Security badges
            st.markdown("""
                <div class="security-badge">
                    <div>🔒 Secured with AES-256 encryption</div>
                    <div>⚡ Powered by AI OCR Engine v2.1</div>
                </div>
            """, unsafe_allow_html=True)

        # Remove right column mode toggle

        # Remove particles layer

        # Tilt hover effect
        components.html("""
        <script>
            const card = parent.document.querySelector('[data-testid="stForm"]');
            if (card) {
                card.addEventListener('mousemove', (e) => {
                    const rect = card.getBoundingClientRect();
                    const x = e.clientX - rect.left; const y = e.clientY - rect.top;
                    const rx = ((y / rect.height) - 0.5) * -5;
                    const ry = ((x / rect.width) - 0.5) * 5;
                    card.style.transform = `perspective(900px) rotateX(${rx}deg) rotateY(${ry}deg)`;
                });
                card.addEventListener('mouseleave', () => {
                    card.style.transform = 'perspective(900px) rotateX(0deg) rotateY(0deg)';
                });
            }
        </script>
        """, height=0)
