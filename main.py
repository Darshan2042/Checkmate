import streamlit as st
from authentication import login_signup
from homepage import homepage
import time

# Page configuration
st.set_page_config(
    page_title="CheckMate - AI Cheque Extractor",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern UI with animations - Fintech Color Scheme
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background gradient */
    .stApp {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        25% { background-position: 100% 50%; }
        50% { background-position: 100% 100%; }
        75% { background-position: 0% 100%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Content container */
    .main .block-container {
        background: #FFFFFF;
        border-radius: 24px;
        padding: 2.5rem;
        box-shadow: 0 20px 60px rgba(37, 99, 235, 0.08);
        backdrop-filter: blur(10px);
        animation: fadeIn 0.8s ease-in;
        border: 1px solid rgba(37, 99, 235, 0.1);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Headings */
    h1 {
        background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        animation: slideInDown 0.8s ease;
        letter-spacing: -0.5px;
    }
    
    @keyframes slideInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    h2, h3 {
        color: #1E40AF;
        font-weight: 700;
    }
    
    p {
        color: #0F172A;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        letter-spacing: 0.3px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.4);
        background: linear-gradient(135deg, #1E40AF 0%, #1E3A8A 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        border: 2px solid #E2E8F0;
        border-radius: 12px;
        padding: 0.75rem;
        transition: all 0.3s ease;
        background: #FFFFFF;
        color: #0F172A;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #2563EB;
        box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1);
    }
    
    /* File uploader */
    .stFileUploader {
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.05) 0%, rgba(30, 64, 175, 0.05) 100%);
        border-radius: 16px;
        padding: 2rem;
        border: 2px dashed #2563EB;
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: #1E40AF;
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.08) 0%, rgba(30, 64, 175, 0.08) 100%);
        transform: scale(1.01);
    }
    
    /* Success/Error/Warning messages */
    .stAlert {
        border-radius: 12px;
        animation: slideInRight 0.5s ease;
        border-left: 4px solid;
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    div[data-baseweb="notification"] {
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Tables */
    .stTable, .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.08);
        animation: zoomIn 0.5s ease;
        border: 1px solid #E2E8F0;
    }
    
    @keyframes zoomIn {
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: rgba(37, 99, 235, 0.03);
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid rgba(37, 99, 235, 0.1);
    }
    
    /* Download buttons special styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #22C55E 0%, #16A34A 100%);
        box-shadow: 0 4px 15px rgba(34, 197, 94, 0.3);
        color: white;
    }
    
    .stDownloadButton > button:hover {
        box-shadow: 0 6px 20px rgba(34, 197, 94, 0.4);
        background: linear-gradient(135deg, #16A34A 0%, #15803D 100%);
        transform: translateY(-2px);
    }
    
    /* Spinner/Loader */
    .stSpinner > div {
        border-color: #2563EB;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #2563EB 0%, #22C55E 100%);
    }
    
    /* Card effect for sections */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
        background: #FFFFFF;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.08);
        margin: 1rem 0;
        transition: all 0.3s ease;
        border: 1px solid #E2E8F0;
    }
    
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"]:hover {
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.12);
        transform: translateY(-2px);
        border-color: rgba(37, 99, 235, 0.2);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F8FAFC;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #1E40AF 0%, #1E3A8A 100%);
    }
    
    /* Toast notifications */
    [data-testid="stToast"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        box-shadow: 0 8px 24px rgba(37, 99, 235, 0.15);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Check authentication status
if not st.session_state["authenticated"]:
    # Render login/signup functionality
    login_signup()
else:
    # Render homepage functionality
    homepage()
