from dotenv import load_dotenv
from PIL import Image
import os
import google.generativeai as genai
import streamlit as st
import io
import csv
import json
from fpdf import FPDF
import pymongo
from bson.objectid import ObjectId
import pandas as pd
import fitz  # PyMuPDF for PDF handling
import time
import sys
import certifi

# Initialize Gemini model (cached to avoid re-initialization)
@st.cache_resource
def initialize_gemini():
    # Try Streamlit secrets first (for cloud), then fall back to .env (for local)
    try:
        key = st.secrets["GOOGLE_API_KEY"]
    except:
        load_dotenv(override=True)
        key = os.getenv("GOOGLE_API_KEY")
    
    if not key or key.strip() == "":
        st.error("❌ Google API Key not found!")
        st.info("Please add your GOOGLE_API_KEY to Streamlit secrets or .env file")
        st.stop()
    
    try:
        genai.configure(api_key=key.strip())
        print(f"✓ Gemini API configured successfully")
    except Exception as e:
        st.error(f"❌ Failed to configure Gemini API: {str(e)}")
        st.info("Please check if your GOOGLE_API_KEY is valid")
        st.stop()
    
    # Try to list available models and use one that works
    try:
        available_models = []
        for model_info in genai.list_models():
            if 'generateContent' in model_info.supported_generation_methods:
                available_models.append(model_info.name)
        
        if available_models:
            print(f"✓ Found {len(available_models)} available Gemini models")
            print(f"  Using: {available_models[0]}")
            model = genai.GenerativeModel(available_models[0])
            return model
    except Exception as e:
        print(f"Warning: Could not list models - {str(e)}")
        pass
    
    # Fallback to known model names
    model_names = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro", "gemini-1.0-pro"]
    for model_name in model_names:
        try:
            print(f"Trying model: {model_name}")
            model = genai.GenerativeModel(model_name)
            print(f"✓ Successfully initialized {model_name}")
            return model
        except Exception as e:
            print(f"  Failed: {str(e)}")
            continue
    
    st.error("❌ Could not initialize any Gemini model")
    st.info("Possible reasons:\n- Invalid API key\n- API not enabled for your account\n- Network connectivity issues")
    st.stop()

# MongoDB setup (optional - only used if saving to database)
@st.cache_resource(ttl=300)  # Cache for 5 minutes
def get_mongodb_client():
    """Get MongoDB client with proper SSL configuration"""
    try:
        # Try Streamlit secrets first (for cloud), then fall back to .env (for local)
        try:
            MONGO_URI = st.secrets["MONGO_URI"]
            print("Using MONGO_URI from Streamlit secrets")
        except:
            load_dotenv(override=True)
            MONGO_URI = os.getenv("MONGO_URI")
            print("Using MONGO_URI from .env file")
        
        if not MONGO_URI:
            print("ERROR: MONGO_URI not found in secrets or .env file")
            return None
        
        # Remove quotes and whitespace if present
        MONGO_URI = MONGO_URI.strip('"').strip("'").strip()
        
        # Remove any line breaks that might be in the URI
        MONGO_URI = MONGO_URI.replace('\n', '').replace('\r', '')
        
        print(f"Attempting MongoDB connection to: {MONGO_URI[:50]}...")
        
        # Try different SSL configurations for Windows compatibility
        try:
            # First attempt: Use system SSL with longer timeout
            client = pymongo.MongoClient(
                MONGO_URI,
                tls=True,
                tlsAllowInvalidCertificates=False,
                serverSelectionTimeoutMS=10000,  # Increased to 10 seconds
                connectTimeoutMS=10000
            )
            # Test connection
            client.admin.command('ping')
            print("MongoDB connected successfully (with valid certificates)")
            return client
        except Exception as e1:
            print(f"First connection attempt failed: {str(e1)[:100]}")
            try:
                # Fallback: Allow invalid certificates for Windows SSL issues
                client = pymongo.MongoClient(
                    MONGO_URI,
                    tls=True,
                    tlsAllowInvalidCertificates=True,
                    serverSelectionTimeoutMS=10000,
                    connectTimeoutMS=10000
                )
                # Test connection
                client.admin.command('ping')
                print("MongoDB connected successfully (allowing invalid certificates)")
                return client
            except Exception as e2:
                print(f"Second connection attempt failed: {str(e2)[:100]}")
                raise
        
    except Exception as e:
        print(f"MongoDB connection error: {str(e)[:200]}")
        import traceback
        print(traceback.format_exc())
        return None

def get_mongodb_collection():
    """Get user-specific MongoDB collection for cheque data"""
    try:
        client = get_mongodb_client()
        if client is None:
            return None
        
        # Get current username from session
        username = st.session_state.get('username', 'default_user')
        
        db = client['checkmate_db']
        # Each user gets their own collection
        collection_name = f'cheques_{username}'
        return db[collection_name]
    except Exception as e:
        print(f"Error getting collection: {str(e)[:200]}")
        return None

def get_user_profile_collection():
    """Get MongoDB collection for user profiles"""
    try:
        client = get_mongodb_client()
        if client is None:
            return None
        
        db = client['checkmate_db']
        return db['user_profiles']
    except Exception as e:
        print(f"Error getting profile collection: {str(e)[:200]}")
        return None

# Get total cheque count from database with caching
@st.cache_data(ttl=60)  # Cache for 1 minute
def get_total_cheque_count(username=None):
    """Get the total number of cheques processed by the user"""
    try:
        if username is None:
            username = st.session_state.get('username', 'default_user')
        
        collection = get_mongodb_collection()
        if collection is not None:
            count = collection.count_documents({})
            return count
        return 0
    except Exception as e:
        print(f"Error getting cheque count: {str(e)[:100]}")
        return 0

# Save user profile to MongoDB
def save_user_profile(profile_data):
    """Save user profile data to MongoDB"""
    try:
        collection = get_user_profile_collection()
        if collection is None:
            print("ERROR: Could not get user profile collection")
            return False
        
        username = st.session_state.get('username', 'default_user')
        print(f"Saving profile for user: {username}")
        
        # Load existing data to preserve password_hash
        existing_data = collection.find_one({'username': username})
        
        # Prepare profile data
        profile_to_save = profile_data.copy()
        
        # Convert photo to base64 for MongoDB storage
        if 'photo' in profile_to_save and profile_to_save['photo']:
            import base64
            if isinstance(profile_to_save['photo'], bytes):
                profile_to_save['photo'] = base64.b64encode(profile_to_save['photo']).decode('utf-8')
        
        profile_to_save['username'] = username
        from datetime import datetime
        profile_to_save['last_updated'] = datetime.now().isoformat()
        
        # Preserve password_hash if it exists in database
        if existing_data and 'password_hash' in existing_data:
            profile_to_save['password_hash'] = existing_data['password_hash']
            print(f"Preserving existing password_hash for {username}")
        
        # Update or insert profile
        result = collection.update_one(
            {'username': username},
            {'$set': profile_to_save},
            upsert=True
        )
        
        print(f"Profile save result - Matched: {result.matched_count}, Modified: {result.modified_count}, Upserted: {result.upserted_id}")
        return True
    except Exception as e:
        print(f"Error saving profile: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

# Load user profile from MongoDB
def load_user_profile():
    """Load user profile data from MongoDB"""
    try:
        collection = get_user_profile_collection()
        if collection is None:
            print("ERROR: Could not get user profile collection for loading")
            return None
        
        username = st.session_state.get('username', 'default_user')
        print(f"Loading profile for user: {username}")
        
        profile = collection.find_one({'username': username})
        
        if profile:
            print(f"Profile found for {username}")
            # Remove MongoDB _id before returning
            if '_id' in profile:
                del profile['_id']
            
            # Convert base64 photo back to bytes
            if 'photo' in profile and profile['photo']:
                import base64
                if isinstance(profile['photo'], str):
                    try:
                        profile['photo'] = base64.b64decode(profile['photo'])
                    except:
                        profile['photo'] = None
            
            return profile
        else:
            print(f"No profile found for {username}")
            return None
    except Exception as e:
        print(f"Error loading profile: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return None

# Save user credentials to MongoDB
def save_user_credentials(username, hashed_password):
    """Save user login credentials to MongoDB"""
    try:
        collection = get_user_profile_collection()
        if collection is None:
            print("ERROR: Could not get user profile collection for credentials")
            return False
        
        print(f"Saving credentials for user: {username}")
        
        from datetime import datetime
        
        # Update or insert credentials
        result = collection.update_one(
            {'username': username},
            {'$set': {
                'username': username,
                'password_hash': hashed_password,
                'last_updated': datetime.now().isoformat()
            }},
            upsert=True
        )
        
        print(f"Credentials save result - Matched: {result.matched_count}, Modified: {result.modified_count}, Upserted: {result.upserted_id}")
        return True
    except Exception as e:
        print(f"Error saving credentials: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

# Load user credentials from MongoDB
def load_user_credentials(username):
    """Load user login credentials from MongoDB"""
    try:
        collection = get_user_profile_collection()
        if collection is None:
            print("ERROR: Could not get user profile collection for loading credentials")
            return None
        
        print(f"Loading credentials for user: {username}")
        
        user = collection.find_one({'username': username})
        
        if user and 'password_hash' in user:
            print(f"Credentials found for {username}")
            return user['password_hash']
        else:
            print(f"No credentials found for {username}")
            return None
    except Exception as e:
        print(f"Error loading credentials: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return None

# Get all usernames from MongoDB
def get_all_usernames():
    """Get list of all registered usernames from MongoDB"""
    try:
        collection = get_user_profile_collection()
        if collection is None:
            print("ERROR: Could not get user profile collection for usernames")
            return []
        
        users = collection.find({}, {'username': 1})
        usernames = [user['username'] for user in users if 'username' in user]
        print(f"Found {len(usernames)} users in MongoDB")
        return usernames
    except Exception as e:
        print(f"Error getting usernames: {str(e)}")
        return []

# Enhanced input prompt
input_prompt = '''
You are an expert in analyzing bank cheques. Given an image of a cheque, extract the following information accurately:
1. Bank Name
2. IFSC Code
3. Cheque Number (6-digit or 8-digit numeric)
4. Payee Name
5. Date of the cheque (in YYYY-MM-DD format)
6. Amount in Words
7. Amount in Numbers (strictly numeric, no commas)
8. Account Number (12 to 18-digit numeric)

Output the data in the exact format below with no extra symbols or placeholders:
"Bank Name: <value>\nIFSC Code: <value>\nCheque Number: <value>\nPayee Name: <value>\nDate: <value>\nAmount (Words): <value>\nAmount (Numbers): <value>\nAccount Number: <value>"
'''

def cheque_extractor_app():
    # Initialize Gemini model
    model = initialize_gemini()
    
    # Initialize session state for caching results and preserving extracted data
    if 'processed_files' not in st.session_state:
        st.session_state.processed_files = {}
    
    if 'last_extracted_data' not in st.session_state:
        st.session_state.last_extracted_data = None
    
    if 'last_uploaded_filename' not in st.session_state:
        st.session_state.last_uploaded_filename = None
    
    # Function to generate Gemini response with retry logic
    def get_gemini_response(input_prompt, image, max_retries=3):
        from google.api_core.exceptions import ResourceExhausted
        
        for attempt in range(max_retries):
            try:
                print(f"Attempt {attempt + 1}/{max_retries}: Calling Gemini API...")
                response = model.generate_content([input_prompt, image[0]])
                if response and hasattr(response, 'text'):
                    print(f"✓ Received response from Gemini (length: {len(response.text)} chars)")
                    return response.text
                else:
                    print(f"✗ No text in response: {response}")
                    return None
            except ResourceExhausted as e:
                error_msg = str(e)
                print(f"✗ API quota exceeded: {error_msg}")
                
                # Extract retry delay if available
                retry_delay = 60  # Default to 60 seconds
                if "retry in" in error_msg.lower():
                    try:
                        import re
                        match = re.search(r'retry in ([0-9.]+)s', error_msg)
                        if match:
                            retry_delay = float(match.group(1))
                    except:
                        pass
                
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    with st.spinner(f"API quota exceeded. Retrying in {retry_delay} seconds..."):
                        time.sleep(retry_delay)
                else:
                    st.error(f"❌ API quota exceeded. Please try again later or check your API limits.")
                    return None
            except Exception as e:
                error_msg = str(e)
                print(f"✗ Gemini API error (attempt {attempt + 1}): {error_msg}")
                
                # Check for specific error types
                if "API_KEY" in error_msg.upper() or "INVALID" in error_msg.upper():
                    st.error(f"❌ Invalid API Key: {error_msg}")
                    return None
                elif "PERMISSION" in error_msg.upper() or "DENIED" in error_msg.upper():
                    st.error(f"❌ Permission denied. Please enable Gemini API in Google Cloud Console.")
                    return None
                
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    st.error(f"❌ Failed after {max_retries} attempts: {error_msg}")
                    return None
        
        return None

    # Prepare image data for Gemini API with optimization
    def input_image_details(image_path):
        try:
            import hashlib
            
            # Optimize image size to reduce API payload
            from PIL import Image
            img = Image.open(image_path)
            
            # Calculate file hash for caching
            with open(image_path, "rb") as img_file:
                file_hash = hashlib.md5(img_file.read()).hexdigest()
            
            # Check cache - return cached string key, not the data
            if file_hash in st.session_state.processed_files:
                return None, file_hash, True  # Return cached flag
            
            # Resize if too large (max 4MB for Gemini)
            max_size = (2048, 2048)
            if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Save optimized image to bytes
                buffered = io.BytesIO()
                img.save(buffered, format="JPEG", quality=85, optimize=True)
                bytes_data = buffered.getvalue()
                mime_type = "image/jpeg"
            else:
                # Read original file
                with open(image_path, "rb") as img_file:
                    bytes_data = img_file.read()
                
                # Detect image type
                if image_path.lower().endswith('.png'):
                    mime_type = "image/png"
                elif image_path.lower().endswith(('.jpg', '.jpeg')):
                    mime_type = "image/jpeg"
                else:
                    mime_type = "image/jpeg"
            
            image_parts = [
                {'mime_type': mime_type, 'data': bytes_data}
            ]
            return image_parts, file_hash, False  # Not cached
        except Exception as e:
            return None, None, False

    # Extract images from PDF
    def extract_images_from_pdf(pdf_path, output_folder):
        pdf_document = fitz.open(pdf_path)
        image_paths = []
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            images = page.get_images(full=True)
            for i, img in enumerate(images):
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image_filename = os.path.join(output_folder, f"page{page_number + 1}_img{i + 1}.png")
                with open(image_filename, "wb") as f:
                    f.write(image_bytes)
                image_paths.append(image_filename)
        return image_paths

    # Parse Gemini response
    def parse_response(response_text):
        data = {}
        for line in response_text.split('\n'):
            if ":" in line:
                key, value = line.split(":", 1)
                data[key.strip()] = value.strip()
        return data

    # Function to display extracted results
    def display_extracted_results(all_extracted_data, output_folder):
        """Display the extracted data with download options"""
        # Clean data for display and export (remove/convert ObjectIds)
        clean_data = []
        for record in all_extracted_data:
            clean_record = {}
            for key, value in record.items():
                if isinstance(value, ObjectId):
                    clean_record[key] = str(value)
                else:
                    clean_record[key] = value
            clean_data.append(clean_record)
        
        df = pd.DataFrame(clean_data)
        st.table(df)
        
        # Save and provide download options
        csv_buffer = io.StringIO()
        json_buffer = io.StringIO()
        
        # Use clean_data (without ObjectIds) for CSV
        if clean_data:
            csv_writer = csv.DictWriter(csv_buffer, fieldnames=clean_data[0].keys())
            csv_writer.writeheader()
            csv_writer.writerows(clean_data)
        
        # JSON export
        json.dump(clean_data, json_buffer, indent=4)
        
        # PDF export
        pdf_filename = os.path.join(output_folder, "cheque_data.pdf")
        save_as_pdf(clean_data[0] if clean_data else {}, pdf_filename)

        st.subheader("📥 Download Options")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.download_button("📄 Download CSV", csv_buffer.getvalue(), "cheque_data.csv", "text/csv", use_container_width=True)
        with col2:
            st.download_button("📋 Download JSON", json_buffer.getvalue(), "cheque_data.json", "application/json", use_container_width=True)
        with col3:
            with open(pdf_filename, "rb") as pdf_file:
                st.download_button("📕 Download PDF", pdf_file.read(), "cheque_data.pdf", "application/pdf", use_container_width=True)

    # Function to save data as PDF
    def save_as_pdf(data, filename):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Cheque Data Extraction", ln=True, align='C')
        pdf.ln(10)
        for key, value in data.items():
            pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
        pdf.output(filename)

    # Streamlit UI setup
    st.subheader('Cheque Data Extractor 🚀 :gemini:')
    
    # Display previously extracted data if exists and no new file is uploaded
    if st.session_state.last_extracted_data is not None and 'uploaded_file' not in locals():
        display_extracted_results(st.session_state.last_extracted_data, output_folder="extracted_cheques")
        
        # Add option to clear and start fresh
        if st.button("🔄 Extract New Cheque"):
            st.session_state.last_extracted_data = None
            st.session_state.last_uploaded_filename = None
            st.rerun()
        return
    
    uploaded_file = st.file_uploader('Upload a cheque image or PDF...', type=['jpg', 'jpeg', 'png', 'pdf'], key='cheque_uploader')
    output_folder = "extracted_cheques"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1].lower()
        if file_extension == "pdf":
            pdf_path = os.path.join(output_folder, uploaded_file.name)
            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            image_paths = extract_images_from_pdf(pdf_path, output_folder)
        else:
            image_path = os.path.join(output_folder, uploaded_file.name)
            with open(image_path, "wb") as img_file:
                img_file.write(uploaded_file.getbuffer())
            image_paths = [image_path]

        all_extracted_data = []
        extraction_errors = []
        
        for img_path in image_paths:
            with st.spinner(f'🔍 Extracting data from {os.path.basename(img_path)}...'):
                try:
                    image_data, file_hash, is_cached = input_image_details(img_path)
                    
                    # Check if we have cached result
                    if is_cached and file_hash in st.session_state.processed_files:
                        parsed_data = st.session_state.processed_files[file_hash]
                        all_extracted_data.append(parsed_data)
                        st.success(f"✓ Loaded cached data for {os.path.basename(img_path)}")
                        continue
                    
                    if image_data is None:
                        error_msg = f"Failed to process image: {os.path.basename(img_path)}"
                        extraction_errors.append(error_msg)
                        st.error(error_msg)
                        continue
                    
                    st.info(f"Sending image to Gemini AI for analysis...")
                    response_text = get_gemini_response(input_prompt, image_data)
                    
                    if response_text:
                        st.success("✓ Received response from Gemini AI")
                        parsed_data = parse_response(response_text)
                        if parsed_data:
                            # Cache the result using json string as key
                            if file_hash:
                                st.session_state.processed_files[file_hash] = parsed_data.copy()
                            all_extracted_data.append(parsed_data)
                            st.success(f"✓ Successfully extracted data from {os.path.basename(img_path)}")
                        else:
                            error_msg = f"Failed to parse Gemini response for {os.path.basename(img_path)}"
                            extraction_errors.append(error_msg)
                            st.error(error_msg)
                            st.code(response_text, language="text")
                    else:
                        error_msg = f"No response from Gemini AI for {os.path.basename(img_path)}. Possible reasons:\n- API quota exceeded\n- Invalid API key\n- Network issues\n- Image format not supported"
                        extraction_errors.append(error_msg)
                        st.error(error_msg)
                        
                except Exception as e:
                    error_msg = f"Error processing {os.path.basename(img_path)}: {str(e)}"
                    extraction_errors.append(error_msg)
                    st.error(error_msg)
                    import traceback
                    st.code(traceback.format_exc(), language="python")
                    continue

        # Show summary of extraction process
        if extraction_errors:
            st.warning(f"⚠️ Extraction completed with {len(extraction_errors)} error(s)")
            with st.expander("View Errors"):
                for error in extraction_errors:
                    st.text(error)
        
        if not all_extracted_data:
            st.error("❌ No data could be extracted from the uploaded file(s)")
            st.info("💡 Tips:\n- Ensure the image is clear and high quality\n- Check if your Google API key is valid\n- Verify you haven't exceeded API quota\n- Try a different cheque image")
            return
        
        # Save to session state for persistence across page navigation
        st.session_state.last_extracted_data = all_extracted_data
        st.session_state.last_uploaded_filename = uploaded_file.name
        
        # Auto-save to database with user profile info
        collection = get_mongodb_collection()
        db_saved = False
        if collection is not None:
            try:
                from datetime import datetime
                
                # Get current user info
                username = st.session_state.get('username', 'default_user')
                
                # Ensure profile_data exists - load from MongoDB if not in session
                if 'profile_data' not in st.session_state:
                    loaded_profile = load_user_profile()
                    if loaded_profile:
                        st.session_state.profile_data = loaded_profile
                    else:
                        # Create default profile if none exists
                        st.session_state.profile_data = {
                            'name': username.capitalize(),
                            'email': f'{username}@checkmate.ai',
                            'phone': '+1 (555) 000-0000'
                        }
                
                user_name = st.session_state.get('profile_data', {}).get('name', username)
                user_email = st.session_state.get('profile_data', {}).get('email', f'{username}@checkmate.ai')
                user_phone = st.session_state.get('profile_data', {}).get('phone', 'N/A')
                
                db_data = []
                for data in all_extracted_data:
                    db_record = data.copy()
                    
                    # Add metadata - IMPORTANT: This links cheque to user
                    db_record['username'] = username  # User identifier
                    db_record['extraction_date'] = datetime.now().isoformat()
                    db_record['extracted_by'] = user_name
                    db_record['user_email'] = user_email
                    db_record['user_phone'] = user_phone
                    db_record['uploaded_filename'] = uploaded_file.name
                    
                    db_data.append(db_record)
                
                # Insert into user-specific collection
                result = collection.insert_many(db_data)
                db_saved = True
                
                # Convert ObjectId to string for JSON serialization
                for i, record in enumerate(db_data):
                    if '_id' in record:
                        all_extracted_data[i]['_id'] = str(record['_id'])
                
                # Also save/update user profile
                save_user_profile(st.session_state.get('profile_data', {}))
                        
            except pymongo.errors.ConnectionFailure as e:
                pass
            except Exception as e:
                pass
        else:
            pass
        
        # Display the results using the reusable function
        display_extracted_results(all_extracted_data, output_folder)
