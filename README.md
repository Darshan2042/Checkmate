# CheckMate-Automated-Cheque-Data-Extractor

## 📝 Description
CheckMate is a Python-based project designed to simplify the process of cheque data extraction and management. Leveraging advanced AI and robust database integration, it provides an efficient, secure, and user-friendly solution for handling cheque-related tasks.

With its ability to extract critical cheque data, ensure secure user authentication, and centralize management, CheckMate aims to reduce human error and increase productivity in cheque processing.

---

## 🚀 Features
- **Cheque Data Extraction**: Automatically extract key details such as bank name, IFSC code, cheque number, payee name, date, amount (in words and numbers), and account number from scanned cheque images or PDFs.
- **PDF Image Extraction**: Handles PDF uploads, extracts images from pages, and processes them for data extraction.
- **AI-Powered**: Uses Google Gemini AI for precise and automated data extraction.
- **Data Management**: Save extracted cheque details in MongoDB, download them as CSV, JSON, or PDF files.
- **Secure User Authentication**: Ensures data privacy using bcrypt for hashing and secure login/signup flows.
- **Streamlit UI**: A clean and interactive web interface for uploading cheques and viewing extracted data.
- **Environment Configurations**: Handles sensitive data using `.env` files.

---

## 🛠️ Technologies Used
- **Python**: Core programming language.
- **Streamlit**: For building an interactive and user-friendly UI.
- **MongoDB**: For centralized data management and storage.
- **PyMuPDF**: For extracting images from PDF files.
- **FPDF**: For generating downloadable PDF reports.
- **Google Gemini AI**: For AI-powered data extraction.
- **bcrypt**: For secure password management.
- **dotenv**: For managing environment variables.
- **pandas**: For tabular data management and visualization.

---

## ⚙️ Installation
Follow these steps to set up and run the project locally:

Step 1: Clone the Repository

git clone https://github.com/GAURAV142004/CheckMate-Cheque-Processor.git
cd CheckMate-Cheque-Processor

---

Step 2: Set Up a Virtual Environment

python -m venv venv
source venv/bin/activate  
---

Step 3: Install Dependencies
pip install -r requirements.txt
---

 Step 4: Set Up Environment Variables
- Create a .env file in the root directory.
- Add the required variables:
GOOGLE_API_KEY=your-google-api-key
SECRET_KEY=your-secret-key
MONGO_URI=your-mongo-db-connection-string
---

step 5: Run the application
python main.py


