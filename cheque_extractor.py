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

# Load environment variables
load_dotenv()
key = os.getenv("GOOGLE_API_KEY")

if not key:
    st.error("GOOGLE_API_KEY not found in .env file. Please add your API key.")
    st.stop()

# Configure Gemini API
genai.configure(api_key=key)
model_name = "gemini-2.5-flash"
try:
    model = genai.GenerativeModel(model_name)
except Exception as e:
    st.error(f"Error loading model {model_name}: {str(e)}")
    st.stop()

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://pawardarshan1204_db_user:e8YWNKRO8G7W7Nf3@cluster0.zr2canz.mongodb.net/")
client = pymongo.MongoClient(MONGO_URI)
db = client['infosys']
collection = db['cheque_data']

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
    # Function to generate Gemini response
    def get_gemini_response(input_prompt, image):
        response = model.generate_content([input_prompt, image[0]])
        return response.text

    # Prepare image data for Gemini API
    def input_image_details(image_path):
        with open(image_path, "rb") as img_file:
            bytes_data = img_file.read()
            image_parts = [
                {'mime_type': "image/jpeg", 'data': bytes_data}
            ]
        return image_parts

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
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(37, 99, 235, 0.08) 0%, rgba(30, 64, 175, 0.08) 100%); 
                padding: 1.5rem; border-radius: 16px; margin-bottom: 2rem; animation: fadeIn 0.8s ease;
                border: 1px solid rgba(37, 99, 235, 0.2);'>
        <h2 style='margin: 0; color: #1E40AF;'>🚀 AI Cheque Data Extractor</h2>
        <p style='margin: 0.5rem 0 0 0; color: #0F172A; font-weight: 500;'>Powered by Google Gemini AI • Upload your cheque and let AI do the magic!</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader('📤 Upload a cheque image or PDF...', type=['jpg', 'jpeg', 'png', 'pdf'], 
                                     help="Supported formats: JPG, JPEG, PNG, PDF")
    output_folder = "extracted_cheques"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if uploaded_file is not None:
        st.toast(f"📄 File uploaded: {uploaded_file.name}", icon="✅")
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
        
        # Processing with progress bar
        st.markdown("### 🔄 Processing your cheque...")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for idx, img_path in enumerate(image_paths):
            status_text.text(f"🤖 AI is analyzing image {idx + 1} of {len(image_paths)}...")
            progress_bar.progress((idx + 1) / len(image_paths))
            
            image_data = input_image_details(img_path)
            response_text = get_gemini_response(input_prompt, image_data)
            parsed_data = parse_response(response_text)
            all_extracted_data.append(parsed_data)
        
        status_text.empty()
        progress_bar.empty()
        
        # Success notification
        st.success("✅ Extraction completed successfully!")
        st.toast("🎉 Cheque data extracted!", icon="✨")
        st.balloons()
        
        # Display results
        st.markdown("### 📊 Extracted Data")
        df = pd.DataFrame(all_extracted_data)
        st.dataframe(df, use_container_width=True)

        # Save and provide download options
        csv_buffer = io.StringIO()
        json_buffer = io.StringIO()
        csv_writer = csv.DictWriter(csv_buffer, fieldnames=all_extracted_data[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(all_extracted_data)
        json.dump(all_extracted_data, json_buffer, indent=4)
        pdf_filename = os.path.join(output_folder, "cheque_data.pdf")
        save_as_pdf(all_extracted_data[0], pdf_filename)

        st.markdown("### 💾 Download Options")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.download_button("📊 CSV", csv_buffer.getvalue(), "cheque_data.csv", "text/csv"):
                st.toast("📊 CSV file ready for download!", icon="💾")
        
        with col2:
            if st.download_button("📋 JSON", json_buffer.getvalue(), "cheque_data.json", "application/json"):
                st.toast("📋 JSON file ready for download!", icon="💾")
        
        with col3:
            with open(pdf_filename, "rb") as pdf_file:
                if st.download_button("📄 PDF", pdf_file.read(), "cheque_data.pdf", "application/pdf"):
                    st.toast("📄 PDF file ready for download!", icon="💾")
        
        with col4:
            if st.button("💾 Save to DB"):
                with st.spinner('Saving to database...'):
                    collection.insert_many(all_extracted_data)
                st.success("✅ Data saved to database successfully!")
                st.toast("💾 Saved to MongoDB!", icon="🎉")
                st.snow()
