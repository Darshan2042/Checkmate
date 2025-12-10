import streamlit as st
from PIL import Image
import io
import time

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
                padding: 1.5rem 2rem;
                margin: 0 auto;
            }

            /* Profile header */
            .profile-header {
                text-align: center;
                padding: 1.5rem;
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
                padding: 1.5rem;
                margin: 1.5rem 0;
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
                width: 200px;
                height: 200px;
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
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])

    with col1:
        if st.button("← Back to Dashboard"):
            st.session_state['current_page'] = 'dashboard'
            st.rerun()
    
    with col2:
        if st.button("🚪 Logout", type="primary", use_container_width=True):
            st.session_state['authenticated'] = False
            st.session_state['current_page'] = 'dashboard'
            st.rerun()

    # Get current username
    username = st.session_state.get('username', 'User')
    
    # Initialize or load profile data from MongoDB
    if 'profile_data' not in st.session_state or st.session_state.get('current_profile_user') != username:
        # Try to load profile from MongoDB
        from cheque_extractor import load_user_profile
        loaded_profile = load_user_profile()
        
        if loaded_profile:
            # Load existing profile from database
            st.session_state.profile_data = loaded_profile
            # Ensure photo field exists (photo is now stored in DB as base64)
            if 'photo' not in st.session_state.profile_data:
                st.session_state.profile_data['photo'] = None
        else:
            # Create new profile for this user
            st.session_state.profile_data = {
                'name': username.capitalize(),
                'email': f'{username}@checkmate.ai',
                'phone': '+1 (555) 000-0000',
                'role': 'Premium User',
                'bio': 'AI-powered cheque processing user',
                'photo': None,
                'joined_date': 'Dec 2024',
                'total_cheques': 0
            }
        
        # Mark which user this profile belongs to
        st.session_state.current_profile_user = username
    
    # Ensure new fields exist in existing profile data
    if 'joined_date' not in st.session_state.profile_data:
        st.session_state.profile_data['joined_date'] = 'Dec 2024'
    
    # Initialize cheque count if not exists
    if 'total_cheques' not in st.session_state.profile_data:
        st.session_state.profile_data['total_cheques'] = 0
    
    # Update cheque count in background (non-blocking)
    try:
        from cheque_extractor import get_total_cheque_count
        # Only update if not recently fetched
        if 'last_count_update' not in st.session_state or \
           (time.time() - st.session_state.get('last_count_update', 0)) > 60:
            st.session_state.profile_data['total_cheques'] = get_total_cheque_count()
            st.session_state.last_count_update = time.time()
    except:
        pass  # Silently fail, use cached value
    
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
    
    
    
    
    # Initialize edit mode state
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = False
    
    # Profile section title with gradient
    st.markdown("""
        <h2 style="margin: 0rem 0 0rem 0; font-size: 1.8rem; font-weight: 999;">
            <span style="background: linear-gradient(90deg, #ec4899, #3b82f6, #22c55e); 
                         -webkit-background-clip: text; 
                         -webkit-text-fill-color: transparent; 
                         background-clip: text;">
                Personal Information
            </span>
        </h2>
    """, unsafe_allow_html=True)
    
    # Edit button
    col_edit1, col_edit2 = st.columns([4, 1])
    with col_edit2:
        if st.button("✏️ Edit" if not st.session_state.edit_mode else "❌ Cancel", use_container_width=True, key="toggle_edit"):
            st.session_state.edit_mode = not st.session_state.edit_mode
            st.rerun()
    
    # Profile content in a single card
    
    
    # Top section: Photo on left, key info on right
    col_photo, col_info = st.columns([1, 2])
    
    with col_photo:
        import base64
        
        # Show file uploader only if no photo exists
        if not st.session_state.profile_data['photo']:
            uploaded_photo = st.file_uploader("Upload Photo", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed", key="photo_uploader")
            
            # Handle photo upload
            if uploaded_photo:
                st.session_state.profile_data['photo'] = uploaded_photo.read()
                st.rerun()
        
        # Display profile photo or placeholder
        photo_html = ""
        if st.session_state.profile_data['photo']:
            try:
                image = Image.open(io.BytesIO(st.session_state.profile_data['photo']))
                buffered = io.BytesIO()
                image.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                photo_html = f'''
                    <div class="profile-photo" style="background-image: url(data:image/png;base64,{img_str}); background-size: cover; background-position: center; font-size: 0; width: 250px; height: 250px; margin: 0 auto;">
                    </div>
                '''
            except:
                photo_html = """<div class="profile-photo" style="width: 250px; height: 250px; margin: 0 auto;">👤</div>"""
        else:
            photo_html = """<div class="profile-photo" style="width: 250px; height: 250px; margin: 0 auto;">👤</div>"""
        
        st.markdown(photo_html, unsafe_allow_html=True)
        
        # Remove photo button (only show in edit mode if photo exists)
        if st.session_state.get('edit_mode', False) and st.session_state.profile_data['photo']:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ Remove Photo", use_container_width=True, key="remove_photo"):
                st.session_state.profile_data['photo'] = None
                st.rerun()
    
    with col_info:
        # Display or edit personal information
        if not st.session_state.edit_mode:
            # Display mode - Grid layout for info
            st.markdown(f"""
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                    <div style="padding: 1rem; background: linear-gradient(135deg, rgba(236,72,153,0.1), rgba(59,130,246,0.1)); border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                        <div style="color: #c7c7d1; font-size: 0.8rem; margin-bottom: 0.4rem; text-transform: uppercase; letter-spacing: 0.5px;">👤 Full Name</div>
                        <div style="color: #ffffff; font-size: 1.1rem; font-weight: 700;">{st.session_state.profile_data['name']}</div>
                    </div>
                    <div style="padding: 1rem; background: linear-gradient(135deg, rgba(59,130,246,0.1), rgba(34,197,94,0.1)); border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                        <div style="color: #c7c7d1; font-size: 0.8rem; margin-bottom: 0.4rem; text-transform: uppercase; letter-spacing: 0.5px;">💼 Role</div>
                        <div style="color: #ffffff; font-size: 1.1rem; font-weight: 700;">{st.session_state.profile_data['role']}</div>
                    </div>
                    <div style="padding: 1rem; background: linear-gradient(135deg, rgba(34,197,94,0.1), rgba(236,72,153,0.1)); border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                        <div style="color: #c7c7d1; font-size: 0.8rem; margin-bottom: 0.4rem; text-transform: uppercase; letter-spacing: 0.5px;">📧 Email</div>
                        <div style="color: #ffffff; font-size: 1.1rem; font-weight: 700;">{st.session_state.profile_data['email']}</div>
                    </div>
                    <div style="padding: 1rem; background: linear-gradient(135deg, rgba(236,72,153,0.1), rgba(59,130,246,0.1)); border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                        <div style="color: #c7c7d1; font-size: 0.8rem; margin-bottom: 0.4rem; text-transform: uppercase; letter-spacing: 0.5px;">📱 Phone</div>
                        <div style="color: #ffffff; font-size: 1.1rem; font-weight: 700;">{st.session_state.profile_data['phone']}</div>
                    </div>
                    <div style="padding: 1rem; background: linear-gradient(135deg, rgba(59,130,246,0.1), rgba(34,197,94,0.1)); border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                        <div style="color: #c7c7d1; font-size: 0.8rem; margin-bottom: 0.4rem; text-transform: uppercase; letter-spacing: 0.5px;">📅 Joined</div>
                        <div style="color: #ffffff; font-size: 1.1rem; font-weight: 700;">{st.session_state.profile_data['joined_date']}</div>
                    </div>
                    <div style="padding: 1rem; background: linear-gradient(135deg, rgba(34,197,94,0.1), rgba(236,72,153,0.1)); border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                        <div style="color: #c7c7d1; font-size: 0.8rem; margin-bottom: 0.4rem; text-transform: uppercase; letter-spacing: 0.5px;">📊 Cheques</div>
                        <div style="color: #ffffff; font-size: 1.1rem; font-weight: 700;">{st.session_state.profile_data['total_cheques']} Processed</div>
                    </div>
                </div>
                <div style="margin-top: 1rem; padding: 1rem; background: linear-gradient(135deg, rgba(236,72,153,0.08), rgba(59,130,246,0.08)); border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                    <div style="color: #c7c7d1; font-size: 0.8rem; margin-bottom: 0.4rem; text-transform: uppercase; letter-spacing: 0.5px;">✍️ Bio</div>
                    <div style="color: #ffffff; font-size: 1rem; font-weight: 600; line-height: 1.6;">{st.session_state.profile_data['bio']}</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Edit mode - show editable inputs in grid layout
        else:
            # Create grid layout similar to display mode
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div style="padding: 0.5rem; background: linear-gradient(135deg, rgba(236,72,153,0.1), rgba(59,130,246,0.1)); border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 1rem;">', unsafe_allow_html=True)
                name = st.text_input("👤 Full Name", value=st.session_state.profile_data['name'], key="profile_name", label_visibility="visible")
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('<div style="padding: 0.5rem; background: linear-gradient(135deg, rgba(34,197,94,0.1), rgba(236,72,153,0.1)); border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 1rem;">', unsafe_allow_html=True)
                email = st.text_input("📧 Email", value=st.session_state.profile_data['email'], key="profile_email", label_visibility="visible")
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('<div style="padding: 0.5rem; background: linear-gradient(135deg, rgba(59,130,246,0.1), rgba(34,197,94,0.1)); border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 1rem;">', unsafe_allow_html=True)
                phone = st.text_input("📱 Phone", value=st.session_state.profile_data['phone'], key="profile_phone", label_visibility="visible")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div style="padding: 0.5rem; background: linear-gradient(135deg, rgba(59,130,246,0.1), rgba(34,197,94,0.1)); border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 1rem;">', unsafe_allow_html=True)
                role = st.text_input("💼 Role", value=st.session_state.profile_data['role'], key="profile_role", label_visibility="visible")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Display-only fields
                st.markdown(f"""
                    <div style="padding: 1rem; background: linear-gradient(135deg, rgba(34,197,94,0.1), rgba(236,72,153,0.1)); border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 1rem;">
                        <div style="color: #c7c7d1; font-size: 0.8rem; margin-bottom: 0.4rem; text-transform: uppercase; letter-spacing: 0.5px;">📅 Joined</div>
                        <div style="color: #ffffff; font-size: 1.1rem; font-weight: 700;">{st.session_state.profile_data['joined_date']}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div style="padding: 1rem; background: linear-gradient(135deg, rgba(236,72,153,0.1), rgba(59,130,246,0.1)); border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 1rem;">
                        <div style="color: #c7c7d1; font-size: 0.8rem; margin-bottom: 0.4rem; text-transform: uppercase; letter-spacing: 0.5px;">📊 Cheques</div>
                        <div style="color: #ffffff; font-size: 1.1rem; font-weight: 700;">{st.session_state.profile_data['total_cheques']} Processed</div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Bio field - full width
            st.markdown('<div style="padding: 0.5rem; background: linear-gradient(135deg, rgba(236,72,153,0.08), rgba(59,130,246,0.08)); border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); margin-top: 1rem;">', unsafe_allow_html=True)
            bio = st.text_area("✍️ Bio", value=st.session_state.profile_data['bio'], height=100, key="profile_bio", label_visibility="visible")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Save button in edit mode
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("💾 Save Changes", use_container_width=True, key="save_in_edit"):
                st.session_state.profile_data['name'] = name
                st.session_state.profile_data['email'] = email
                st.session_state.profile_data['phone'] = phone
                st.session_state.profile_data['role'] = role
                st.session_state.profile_data['bio'] = bio
                
                # Save to MongoDB
                from cheque_extractor import save_user_profile
                if save_user_profile(st.session_state.profile_data):
                    st.success("✅ Profile updated and saved to database!")
                else:
                    st.success("✅ Profile updated locally!")
                    st.info("💡 Profile will be saved to database when you extract a cheque.")
                
                st.session_state.edit_mode = False
                st.balloons()
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)