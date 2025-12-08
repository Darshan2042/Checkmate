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
    # Load environment variables fresh
    load_dotenv(override=True)
    key = os.getenv("GOOGLE_API_KEY")
    
    if not key or key.strip() == "":
        st.error("❌ GOOGLE_API_KEY not found in .env file. Please add your API key from https://aistudio.google.com/app/apikey")
        st.stop()
    
    try:
        genai.configure(api_key=key.strip())
    except Exception as e:
        st.error(f"❌ Failed to configure Gemini API: {str(e)}")
        st.error(f"Current API Key (first 10 chars): {key[:10]}...")
        st.stop()
    
    # Try to list available models and use one that works
    try:
        available_models = []
        for model_info in genai.list_models():
            if 'generateContent' in model_info.supported_generation_methods:
                available_models.append(model_info.name)
        
        if available_models:
            model = genai.GenerativeModel(available_models[0])
            return model
    except:
        pass
    
    # Fallback to known model names
    for model_name in ["gemini-pro", "gemini-1.0-pro", "gemini-1.5-flash"]:
        try:
            model = genai.GenerativeModel(model_name)
            return model
        except:
            continue
    
    st.error("Could not load any Gemini model. Please check your API key.")
    st.stop()

# MongoDB setup (optional - only used if saving to database)
def get_mongodb_collection():
    """Get MongoDB collection with proper SSL configuration"""
    try:
        load_dotenv(override=True)
        MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://pawardarshan1204_db_user:e8YWNKRO8G7W7Nf3@cluster0.zr2canz.mongodb.net/")
        
        # Configure MongoDB client with proper SSL/TLS settings
        client = pymongo.MongoClient(
            MONGO_URI,
            tlsCAFile=certifi.where(),  # Use certifi for SSL certificates
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=10000,
            socketTimeoutMS=10000,
            retryWrites=True,
            w='majority'
        )
        
        # Test connection
        client.admin.command('ping')
        db = client['infosys']
        return db['cheque_data']
    except Exception as e:
        print(f"MongoDB connection error: {str(e)}")
        return None

# Get total cheque count from database
def get_total_cheque_count():
    """Get the total number of cheques processed from the database"""
    try:
        collection = get_mongodb_collection()
        if collection is not None:
            count = collection.count_documents({})
            return count
        return 0
    except Exception as e:
        print(f"Error getting cheque count: {str(e)}")
        return 0

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
                response = model.generate_content([input_prompt, image[0]])
                if response and hasattr(response, 'text'):
                    return response.text
                else:
                    st.error("Empty response from Gemini API")
                    return None
            except ResourceExhausted as e:
                error_msg = str(e)
                
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
                    st.warning(f"⏳ Rate limit reached. Waiting {int(retry_delay)} seconds before retry... (Attempt {attempt + 1}/{max_retries})")
                    
                    # Show countdown
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for i in range(int(retry_delay)):
                        remaining = int(retry_delay) - i
                        progress = (i + 1) / retry_delay
                        progress_bar.progress(progress)
                        status_text.text(f"Retrying in {remaining} seconds...")
                        time.sleep(1)
                    
                    progress_bar.empty()
                    status_text.empty()
                    st.info("🔄 Retrying now...")
                else:
                    st.error("❌ Rate limit exceeded. Please try again later.")
                    st.info("💡 **Tip:** The free tier has a limit of 5 requests per minute. Wait a minute and try again.")
                    return None
            except Exception as e:
                st.error(f"❌ Error: {str(e)[:200]}")
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                    st.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
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
            st.error(f"Error reading image file: {str(e)}")
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
        df = pd.DataFrame(all_extracted_data)
        st.success("✅ Data extracted successfully!")
        st.table(df)
        
        # Clean data for JSON export (remove any MongoDB ObjectIds)
        json_data = []
        for record in all_extracted_data:
            clean_record = {}
            for key, value in record.items():
                if key == '_id':
                    if isinstance(value, ObjectId):
                        clean_record[key] = str(value)
                    else:
                        clean_record[key] = value
                else:
                    clean_record[key] = value
            json_data.append(clean_record)
        
        # Save and provide download options
        csv_buffer = io.StringIO()
        json_buffer = io.StringIO()
        csv_writer = csv.DictWriter(csv_buffer, fieldnames=all_extracted_data[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(all_extracted_data)
        json.dump(json_data, json_buffer, indent=4)
        pdf_filename = os.path.join(output_folder, "cheque_data.pdf")
        save_as_pdf(all_extracted_data[0], pdf_filename)

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
        st.info(f"📋 Showing previously extracted data from: **{st.session_state.last_uploaded_filename}**")
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
        for img_path in image_paths:
            with st.spinner(f'🔍 Extracting data from {os.path.basename(img_path)}...'):
                try:
                    image_data, file_hash, is_cached = input_image_details(img_path)
                    
                    # Check if we have cached result
                    if is_cached and file_hash in st.session_state.processed_files:
                        parsed_data = st.session_state.processed_files[file_hash]
                        all_extracted_data.append(parsed_data)
                        continue
                    
                    if image_data is None:
                        st.warning(f"Failed to read image: {os.path.basename(img_path)}")
                        continue
                    
                    response_text = get_gemini_response(input_prompt, image_data)
                    if response_text:
                        parsed_data = parse_response(response_text)
                        if parsed_data:
                            # Cache the result using json string as key
                            if file_hash:
                                st.session_state.processed_files[file_hash] = parsed_data.copy()
                            all_extracted_data.append(parsed_data)
                        else:
                            st.warning(f"⚠️ Failed to parse data from {os.path.basename(img_path)}")
                    else:
                        st.warning(f"⚠️ No response from API for {os.path.basename(img_path)}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)[:150]}")
                    import traceback
                    st.code(traceback.format_exc())
                    continue

        if not all_extracted_data:
            st.error("❌ No data could be extracted from the uploaded file(s).")
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
                
                # Get user profile data
                user_name = st.session_state.get('profile_data', {}).get('name', 'Unknown User')
                user_email = st.session_state.get('profile_data', {}).get('email', 'no-email@example.com')
                user_phone = st.session_state.get('profile_data', {}).get('phone', 'N/A')
                
                db_data = []
                for data in all_extracted_data:
                    db_record = data.copy()
                    
                    # Add metadata
                    db_record['extraction_date'] = datetime.now().isoformat()
                    db_record['extracted_by'] = user_name
                    db_record['user_email'] = user_email
                    db_record['user_phone'] = user_phone
                    db_record['uploaded_filename'] = uploaded_file.name
                    
                    db_data.append(db_record)
                
                # Insert into MongoDB
                result = collection.insert_many(db_data)
                st.success(f"💾 Successfully saved {len(result.inserted_ids)} record(s) to database!")
                db_saved = True
                
                # Convert ObjectId to string for JSON serialization
                for i, record in enumerate(db_data):
                    if '_id' in record:
                        all_extracted_data[i]['_id'] = str(record['_id'])
                        
            except pymongo.errors.ConnectionFailure as e:
                st.error(f"❌ Database connection failed. Please check your internet connection.")
                st.info("💡 Data will still be available for download below.")
            except Exception as e:
                st.error(f"❌ Database save failed: {str(e)[:150]}")
                st.info("💡 Data will still be available for download below.")
        else:
            st.warning("⚠️ Database connection unavailable. Data not saved to cloud.")
            st.info("💡 You can still download the data using the buttons below.")
        
        # Display the results using the reusable function
        display_extracted_results(all_extracted_data, output_folder)
