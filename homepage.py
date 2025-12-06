from cheque_extractor import cheque_extractor_app
import streamlit as st

def homepage():
    # Apply premium unified AI-powered theme with animations
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

            /* Background with slow-moving gradients */
            .stApp {
                background:
                    radial-gradient(circle at 20% 20%, rgba(236,72,153,0.22) 0%, transparent 35%),
                    radial-gradient(circle at 80% 30%, rgba(59,130,246,0.22) 0%, transparent 35%),
                    radial-gradient(circle at 50% 80%, rgba(34,197,94,0.22) 0%, transparent 40%),
                    linear-gradient(135deg, var(--bg-dark) 0%, var(--bg-dark-2) 100%);
                min-height: 100vh;
                animation: backgroundShift 20s ease infinite alternate;
            }

            @keyframes backgroundShift {
                0% { background-position: 0% 0%; }
                100% { background-position: 100% 100%; }
            }

            /* Floating particles */
            .particles {
                position: fixed;
                width: 100%;
                height: 100%;
                top: 0;
                left: 0;
                pointer-events: none;
                z-index: 0;
            }

            .particle {
                position: absolute;
                width: 3px;
                height: 3px;
                background: rgba(236,72,153,0.3);
                border-radius: 50%;
                animation: float 15s infinite ease-in-out;
            }

            @keyframes float {
                0%, 100% { transform: translateY(0) translateX(0); opacity: 0; }
                10% { opacity: 0.5; }
                50% { transform: translateY(-100vh) translateX(50px); opacity: 0.3; }
                90% { opacity: 0.5; }
            }

            /* Main container - unified padding and centering */
            .main .block-container {
                max-width: 900px;
                padding: 2rem 3rem;
                margin: 0 auto;
            }

            /* Premium header with glow and animations */
            .main-header {
                text-align: center;
                padding: 2.5rem 2rem;
                background: linear-gradient(135deg, rgba(236,72,153,0.15), rgba(59,130,246,0.15));
                border-radius: 20px;
                margin-bottom: 2.5rem;
                backdrop-filter: blur(16px);
                border: 1px solid rgba(255,255,255,0.15);
                position: relative;
                overflow: hidden;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3), inset 0 1px 4px rgba(255,255,255,0.1);
            }

            /* Animated glow behind header */
            .main-header::before {
                content: "";
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(236,72,153,0.3) 0%, transparent 70%);
                animation: glowPulse 6s ease-in-out infinite;
            }

            @keyframes glowPulse {
                0%, 100% { opacity: 0.3; transform: scale(1); }
                50% { opacity: 0.6; transform: scale(1.1); }
            }

            /* Gradient highlight passing across title */
            .gradient-text {
                background: linear-gradient(90deg, #ec4899, #3b82f6, #22c55e, #ec4899);
                background-size: 300% 100%;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                animation: gradientShift 8s linear infinite;
                position: relative;
                z-index: 1;
            }

            @keyframes gradientShift {
                0% { background-position: 0% 50%; }
                100% { background-position: 300% 50%; }
            }

            /* Animated underline */
            .header-underline {
                height: 3px;
                width: 0;
                background: linear-gradient(90deg, transparent, #ec4899, #3b82f6, transparent);
                margin: 1rem auto 0;
                animation: underlineExpand 3s ease-in-out infinite;
            }

            @keyframes underlineExpand {
                0%, 100% { width: 0; }
                50% { width: 60%; }
            }

            /* Welcome message with shimmer */
            .welcome-message {
                text-align: left;
                margin: 0;
                padding: 1rem 0 1.5rem 0;
                position: relative;
            }

            .username-shimmer {
                color: #ec4899;
                font-weight: 800;
                background: linear-gradient(90deg, #ec4899, #f472b6, #ec4899);
                background-size: 200% 100%;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: shimmer 3s ease infinite;
            }

            @keyframes shimmer {
                0%, 100% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
            }

            /* Waving hand animation */
            .wave-hand {
                display: inline-block;
                animation: wave 2s ease-in-out infinite;
                transform-origin: 70% 70%;
            }

            @keyframes wave {
                0%, 100% { transform: rotate(0deg); }
                10%, 30% { transform: rotate(14deg); }
                20% { transform: rotate(-8deg); }
                40%, 100% { transform: rotate(0deg); }
            }

            /* Section card with corner accents */
            .section-card {
                position: relative;
                background: rgba(255,255,255,0.08);
                border: 1px solid rgba(255,255,255,0.22);
                border-radius: 20px;
                padding: 2.5rem;
                margin: 2rem 0;
                backdrop-filter: blur(16px);
                box-shadow: inset 0 1px 4px rgba(255,255,255,0.08), 0 12px 30px rgba(0,0,0,0.35);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }

            .section-card:hover {
                transform: translateY(-2px);
                box-shadow: inset 0 1px 4px rgba(255,255,255,0.12), 0 16px 40px rgba(0,0,0,0.4);
            }

            /* Glowing corner accents */
            .corner-accent {
                position: absolute;
                width: 20px;
                height: 20px;
                border: 2px solid;
                border-color: transparent;
                animation: cornerGlow 3s ease-in-out infinite;
            }

            .corner-accent.top-left { top: -1px; left: -1px; border-top-color: #ec4899; border-left-color: #ec4899; border-top-left-radius: 20px; }
            .corner-accent.top-right { top: -1px; right: -1px; border-top-color: #3b82f6; border-right-color: #3b82f6; border-top-right-radius: 20px; }
            .corner-accent.bottom-left { bottom: -1px; left: -1px; border-bottom-color: #22c55e; border-left-color: #22c55e; border-bottom-left-radius: 20px; }
            .corner-accent.bottom-right { bottom: -1px; right: -1px; border-bottom-color: #ec4899; border-right-color: #ec4899; border-bottom-right-radius: 20px; }

            @keyframes cornerGlow {
                0%, 100% { opacity: 0.6; filter: drop-shadow(0 0 2px currentColor); }
                50% { opacity: 1; filter: drop-shadow(0 0 6px currentColor); }
            }

            /* Section subtitle with pulsing icons */
            .section-subtitle {
                text-align: center;
                color: var(--muted);
                font-size: 0.95rem;
                margin-bottom: 1.5rem;
                letter-spacing: 0.5px;
            }

            .pulse-icon {
                display: inline-block;
                margin: 0 0.3rem;
                animation: iconPulse 2s ease-in-out infinite;
            }

            @keyframes iconPulse {
                0%, 100% { opacity: 0.7; transform: scale(1); }
                50% { opacity: 1; transform: scale(1.15); }
            }

            /* Premium file uploader with animated border - VERTICAL CARD */
            [data-testid="stFileUploader"] {
                background: rgba(255,255,255,0.08);
                border: 2px solid rgba(255,255,255,0.22);
                border-radius: 20px;
                padding: 2rem;
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                box-shadow: inset 0 1px 4px rgba(255,255,255,0.08), 0 12px 30px rgba(0,0,0,0.35);
                transition: all 0.3s ease;
                position: relative;
                overflow: visible;
            }

            [data-testid="stFileUploader"]::before {
                content: "";
                position: absolute;
                inset: -2px;
                border-radius: 20px;
                padding: 2px;
                background: linear-gradient(135deg, #ec4899, #3b82f6, #22c55e);
                -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
                -webkit-mask-composite: xor;
                mask-composite: exclude;
                animation: borderFlow 8s linear infinite;
                opacity: 0.5;
                pointer-events: none;
            }

            [data-testid="stFileUploader"]:hover {
                transform: translateY(-4px) scale(1.01);
                box-shadow: inset 0 1px 4px rgba(255,255,255,0.12), 0 20px 40px rgba(236,72,153,0.2);
            }

            [data-testid="stFileUploader"]:hover::before {
                opacity: 0.8;
            }

            @keyframes borderFlow {
                0% { filter: hue-rotate(0deg); }
                100% { filter: hue-rotate(360deg); }
            }

            /* Typography */
            h1, h2, h3, p, label { color: var(--text) !important; font-weight: 700 !important; }
            .muted { color: var(--muted); font-weight: 600; }

            /* Buttons with animations */
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
                position: relative;
                overflow: hidden;
            }

            .stButton > button::before {
                content: "";
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                transition: left 0.5s ease;
            }

            .stButton > button:hover::before {
                left: 100%;
            }

            .stButton > button:hover {
                transform: translateY(-2px) scale(1.02);
                box-shadow: 0 12px 26px rgba(139,92,246,0.4);
            }

            .stButton > button:active {
                transform: scale(0.98);
            }

            /* Status bar at bottom */
            .status-bar {
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                background: rgba(20,20,37,0.95);
                backdrop-filter: blur(12px);
                padding: 0.8rem 2rem;
                border-top: 1px solid rgba(255,255,255,0.1);
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 0.85rem;
                color: var(--muted);
                z-index: 1000;
            }

            .status-indicator {
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }

            .status-dot {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #22c55e;
                animation: statusPulse 2s ease-in-out infinite;
            }

            @keyframes statusPulse {
                0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(34,197,94,0.7); }
                50% { opacity: 0.8; box-shadow: 0 0 0 4px rgba(34,197,94,0); }
            }

            /* Loading shimmer effect */
            .loading-shimmer {
                background: linear-gradient(90deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.15) 50%, rgba(255,255,255,0.05) 100%);
                background-size: 200% 100%;
                animation: shimmerLoad 2s infinite;
            }

            @keyframes shimmerLoad {
                0% { background-position: -200% 0; }
                100% { background-position: 200% 0; }
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Add floating particles
    st.markdown("""
        <div class="particles">
            <div class="particle" style="left: 10%; animation-delay: 0s;"></div>
            <div class="particle" style="left: 30%; animation-delay: 2s;"></div>
            <div class="particle" style="left: 50%; animation-delay: 4s;"></div>
            <div class="particle" style="left: 70%; animation-delay: 6s;"></div>
            <div class="particle" style="left: 90%; animation-delay: 8s;"></div>
        </div>
    """, unsafe_allow_html=True)
    
    # Welcome message with profile button at same level
    if "username" in st.session_state:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
                <div class="welcome-message">
                    <h2 style='color: #ffffff; font-size: 1.5rem; margin: 0;'>
                        Welcome back, <span class="username-shimmer">{st.session_state["username"]}</span>! 
                        <span class="wave-hand">👋</span>
                    </h2>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("👤 My Profile", key="nav_profile_top", use_container_width=True):
                st.session_state['current_page'] = 'profile'
                st.rerun()
    
    # Premium header with animations
    st.markdown("""
        <div class="main-header">
            <h1 class="gradient-text" style='margin:0; font-size: 2.5rem;'>
                📄 Cheque Data Extractor
            </h1>
            <div class="header-underline"></div>
            <div class="section-subtitle">
                <span class="pulse-icon">🤖</span> AI OCR
                <span style="margin: 0 0.5rem;">•</span>
                <span class="pulse-icon">🛡️</span> Fraud Checks
                <span style="margin: 0 0.5rem;">•</span>
                <span class="pulse-icon">🔍</span> MICR Extraction
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Section card with corner accents and subtitle
    # st.markdown("""
    #     <div style="position: relative; margin: 2rem 0;">
    #         <div class="corner-accent top-left"></div>
    #         <div class="corner-accent top-right"></div>
    #         <div class="corner-accent bottom-left"></div>
    #         <div class="corner-accent bottom-right"></div>
    #         <h2 style='text-align: center; color: #ffffff; margin-bottom: 0.5rem;'>📄 Cheque Data Extractor</h2>
    #         <div class="section-subtitle">
    #             <span class="pulse-icon">🤖</span> AI OCR
    #             <span style="margin: 0 0.5rem;">•</span>
    #             <span class="pulse-icon">🛡️</span> Fraud Checks
    #             <span style="margin: 0 0.5rem;">•</span>
    #             <span class="pulse-icon">🔍</span> MICR Extraction
    #         </div>
    #     </div>
    # """, unsafe_allow_html=True)
    
    # Render the cheque extractor app
    cheque_extractor_app()
    
    # Status bar at bottom
    st.markdown("""
        <div class="status-bar">
            <div class="status-indicator">
                🔒 All uploads are encrypted (AES-256)
            </div>
            <div class="status-indicator">
                <span class="status-dot"></span>
                <span>AI Engine Active</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

