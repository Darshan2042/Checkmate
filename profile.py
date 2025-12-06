import streamlit as st
from PIL import Image
import io

def profile_page():
    # Apply premium theme matching dashboard
    st.markdown("""
        <style>
            :root {
                --bg-dark: #0b0b0f;
                --bg-dark-2: #141425;
                --accent-pink: #ec4899;
                --accent-blue: #3b82f6;
                --accent-green: #22c55e;
                --text: #ffffff;
                --muted: #c7c7d1;
            }

            /* Background */
            .stApp {
                background:
                    radial-gradient(circle at 20% 20%, rgba(236,72,153,0.22) 0%, transparent 35%),
                    radial-gradient(circle at 80% 30%, rgba(59,130,246,0.22) 0%, transparent 35%),
                    radial-gradient(circle at 50% 80%, rgba(34,197,94,0.22) 0%, transparent 40%),
                    linear-gradient(135deg, var(--bg-dark) 0%, var(--bg-dark-2) 100%);
                min-height: 100vh;
            }

            /* Main container */
            .main .block-container {
                max-width: 800px;
                padding: 2rem 3rem;
                margin: 0 auto;
            }

            /* Profile header */
            .profile-header {
                text-align: center;
                padding: 2rem;
                background: linear-gradient(135deg, rgba(236,72,153,0.15), rgba(59,130,246,0.15));
                border-radius: 20px;
                margin-bottom: 2.5rem;
                backdrop-filter: blur(16px);
                border: 1px solid rgba(255,255,255,0.15);
                box-shadow: 0 8px 32px rgba(0,0,0,0.3), inset 0 1px 4px rgba(255,255,255,0.1);
            }

            .gradient-text {
                background: linear-gradient(90deg, #ec4899, #3b82f6, #22c55e);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }

            /* Frosted-glass profile card */
            .profile-card {
                position: relative;
                background: rgba(255,255,255,0.08);
                border: 1px solid rgba(255,255,255,0.22);
                border-radius: 20px;
                padding: 2.5rem;
                margin: 2rem 0;
                backdrop-filter: blur(16px);
                box-shadow: inset 0 1px 4px rgba(255,255,255,0.08), 0 12px 30px rgba(0,0,0,0.35);
            }

            /* Profile photo container */
            .profile-photo-container {
                display: flex;
                justify-content: center;
                margin-bottom: 2rem;
            }

            .profile-photo {
                width: 150px;
                height: 150px;
                border-radius: 50%;
                border: 4px solid;
                border-image: linear-gradient(135deg, #ec4899, #3b82f6) 1;
                box-shadow: 0 8px 24px rgba(236,72,153,0.3);
                object-fit: cover;
                background: linear-gradient(135deg, rgba(236,72,153,0.2), rgba(59,130,246,0.2));
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 4rem;
                cursor: pointer;
                transition: all 0.3s ease;
                position: relative;
            }

            .profile-photo:hover {
                transform: scale(1.05);
                box-shadow: 0 12px 32px rgba(236,72,153,0.5);
            }

            .profile-photo::after {
                content: "📷";
                position: absolute;
                bottom: 10px;
                right: 10px;
                background: linear-gradient(135deg, #ec4899, #8b5cf6);
                border-radius: 50%;
                width: 35px;
                height: 35px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1rem;
                opacity: 0;
                transition: opacity 0.3s ease;
            }

            .profile-photo:hover::after {
                opacity: 1;
            }

            /* Input fields */
            .stTextInput > div > div > input,
            .stTextArea > div > div > textarea {
                background: rgba(255,255,255,0.10);
                color: var(--text);
                border: 2px solid rgba(200,200,210,0.45);
                border-radius: 12px;
                padding: 8px 12px;
                transition: all 150ms ease-in-out;
            }

            .stTextInput > div > div > input:focus,
            .stTextArea > div > div > textarea:focus {
                outline: none;
                border-image: linear-gradient(90deg, var(--accent-pink), var(--accent-blue)) 1;
                box-shadow: 0 0 0 3px rgba(236,72,153,0.22), 0 0 0 6px rgba(59,130,246,0.15);
            }

            /* Buttons */
            .stButton > button {
                font-weight: 800;
                letter-spacing: 0.2px;
                border-radius: 14px !important;
                padding: 0.8rem 1.5rem;
                box-shadow: 0 8px 18px rgba(0,0,0,0.35);
                transition: all 0.2s ease;
                background: linear-gradient(135deg, #ec4899, #8b5cf6) !important;
                border: none;
                color: white !important;
            }

            .stButton > button:hover {
                transform: translateY(-2px) scale(1.02);
                box-shadow: 0 12px 26px rgba(139,92,246,0.4);
            }

            /* Section titles */
            .section-title {
                color: var(--text);
                font-size: 1.2rem;
                font-weight: 700;
                margin-bottom: 1rem;
                padding-bottom: 0.5rem;
                border-bottom: 2px solid;
                border-image: linear-gradient(90deg, #ec4899, #3b82f6) 1;
            }

            /* Info badge */
            .info-badge {
                display: inline-block;
                background: linear-gradient(135deg, rgba(236,72,153,0.2), rgba(59,130,246,0.2));
                border: 1px solid rgba(255,255,255,0.2);
                padding: 0.4rem 1rem;
                border-radius: 20px;
                font-size: 0.85rem;
                color: var(--text);
                margin: 0.2rem;
            }

            /* Typography */
            h1, h2, h3, p, label { color: var(--text) !important; }
            
            /* Hide file uploader */
            .hidden-uploader {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state for profile data
    if 'profile_data' not in st.session_state:
        st.session_state.profile_data = {
            'name': st.session_state.get('username', 'User'),
            'email': 'user@checkmate.ai',
            'phone': '+1 (555) 123-4567',
            'role': 'Premium User',
            'bio': 'AI-powered cheque processing enthusiast',
            'photo': None
        }
    
    # Profile header
    st.markdown("""
        <div class="profile-header">
            <h1 class="gradient-text" style='margin:0; font-size: 2.5rem;'>
                👤 My Profile
            </h1>
            <p style='margin:0.5rem 0 0 0; color: #c7c7d1;'>Manage your account settings</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Back to Dashboard"):
            st.session_state['current_page'] = 'dashboard'
            st.rerun()
    
    with col2:
        if st.button("🚪 Logout", type="primary"):
            st.session_state['authenticated'] = False
            st.session_state['current_page'] = 'dashboard'
            st.rerun()
    
    # Profile card
    # st.markdown('<div class="profile-card">', unsafe_allow_html=True)
    
    # Profile photo section
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="profile-photo-container">', unsafe_allow_html=True)
        
        # Hidden file uploader
        uploaded_photo = st.file_uploader("Upload Photo", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed", key="photo_uploader")
        
        # Display profile photo or placeholder with click handler
        photo_html = ""
        if st.session_state.profile_data['photo']:
            try:
                image = Image.open(io.BytesIO(st.session_state.profile_data['photo']))
                # Save image temporarily to display
                import base64
                buffered = io.BytesIO()
                image.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                photo_html = f'''
                    <div class="profile-photo" onclick="document.querySelector('[data-testid=\\'stFileUploader\\'] input').click()" style="background-image: url(data:image/png;base64,{img_str}); background-size: cover; background-position: center; font-size: 0;">
                    </div>
                '''
            except:
                photo_html = """<div class="profile-photo" onclick="document.querySelector('[data-testid=\\"stFileUploader\\"] input').click()">👤</div>"""
        else:
            photo_html = """<div class="profile-photo" onclick="document.querySelector('[data-testid=\\"stFileUploader\\"] input').click()">👤</div>"""
        
        st.markdown(photo_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Handle photo upload
        if uploaded_photo:
            st.session_state.profile_data['photo'] = uploaded_photo.read()
            st.rerun()
    
    with col2:
        # User info badges
        st.markdown(f"""
            <div style="margin-top: 2rem;">
                <span class="info-badge">🎖️ {st.session_state.profile_data['role']}</span>
                <span class="info-badge">📧 Verified</span>
                <span class="info-badge">⚡ Active</span>
            </div>
        """, unsafe_allow_html=True)
    
    # st.markdown('</div>', unsafe_allow_html=True)
    
    # Editable profile information
    st.markdown('<div class="section-title">📝 Personal Information</div>', unsafe_allow_html=True)
    
    # Create two columns for form fields
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name", value=st.session_state.profile_data['name'], key="profile_name")
        email = st.text_input("Email", value=st.session_state.profile_data['email'], key="profile_email")
    
    with col2:
        phone = st.text_input("Phone", value=st.session_state.profile_data['phone'], key="profile_phone")
        role = st.text_input("Role", value=st.session_state.profile_data['role'], key="profile_role")
    
    bio = st.text_area("Bio", value=st.session_state.profile_data['bio'], height=100, key="profile_bio")
    
    # Save changes and logout buttons
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state['authenticated'] = False
            st.session_state['current_page'] = 'dashboard'
            st.rerun()
    
    with col2:
        if st.button("💾 Save Changes", use_container_width=True):
            # Update profile data
            st.session_state.profile_data['name'] = name
            st.session_state.profile_data['email'] = email
            st.session_state.profile_data['phone'] = phone
            st.session_state.profile_data['role'] = role
            st.session_state.profile_data['bio'] = bio
            
            st.success("✅ Profile updated successfully!")
            st.balloons()
