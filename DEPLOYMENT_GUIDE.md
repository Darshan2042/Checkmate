# CheckMate Deployment Guide

## ✅ Production-Ready Features

### Database Integration
- **MongoDB Atlas** connection with proper SSL/TLS certificates
- **Auto-save** all extracted cheque data to cloud database
- **User tracking** - Each cheque record includes:
  - User name
  - User email
  - User phone
  - Extraction timestamp
  - Uploaded filename
  - All cheque details (Bank, IFSC, Amount, Date, etc.)

### Data Saved to MongoDB
Every extracted cheque is automatically saved with:
```json
{
  "Bank Name": "...",
  "IFSC Code": "...",
  "Cheque Number": "...",
  "Payee Name": "...",
  "Date": "...",
  "Amount (Words)": "...",
  "Amount (Numbers)": "...",
  "Account Number": "...",
  "extraction_date": "2024-12-08T10:30:45.123456",
  "extracted_by": "John Doe",
  "user_email": "john@example.com",
  "user_phone": "+1234567890",
  "uploaded_filename": "cheque_001.jpg"
}
```

## 🚀 Deployment Steps

### 1. Environment Variables
Ensure your `.env` file contains:
```env
GOOGLE_API_KEY="your_gemini_api_key"
SECRET_KEY="your_secret_key_for_authentication"
MONGO_URI="mongodb+srv://username:password@cluster.mongodb.net/"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Required Packages (requirements.txt)
- streamlit>=1.32.0
- pymongo[srv]==4.7.0
- bcrypt==4.0.1
- python-dotenv==1.0.0
- Pillow>=10.0.0
- google-generativeai>=0.8.0
- fpdf==1.7.2
- pandas>=2.1.0
- PyMuPDF>=1.24.0
- certifi
- dnspython

### 4. Deploy to Streamlit Cloud

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Production ready deployment"
   git push origin main
   ```

2. **Streamlit Cloud Setup**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select `main.py` as entry point
   - Add secrets in the Streamlit Cloud dashboard:
     ```toml
     GOOGLE_API_KEY = "your_api_key"
     SECRET_KEY = "your_secret_key"
     MONGO_URI = "mongodb+srv://..."
     ```

3. **Deploy**
   - Click "Deploy"
   - Your app will be live at `https://your-app.streamlit.app`

### 5. Alternative: Deploy to Other Platforms

#### Heroku
```bash
# Create Procfile
echo "web: streamlit run main.py --server.port=$PORT" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

#### AWS EC2 / DigitalOcean
```bash
# Install dependencies
pip install -r requirements.txt

# Run with nohup
nohup streamlit run main.py --server.port=8501 &
```

## 🔒 Security Considerations

1. **Never commit `.env` file** - Add to `.gitignore`
2. **Use environment variables** for all secrets
3. **MongoDB IP Whitelist** - Allow access from deployment platform
4. **SSL/TLS enabled** - Certificate validation with certifi

## 📊 Database Schema

### Collection: `cheque_data`
- Database: `infosys`
- Auto-indexed by `_id`
- Searchable by user_email, extraction_date, uploaded_filename

## 🎯 Features for Production

✅ SSL/TLS secure MongoDB connection
✅ Automatic data persistence
✅ User profile integration
✅ Error handling and retry logic
✅ Rate limit management
✅ File caching for performance
✅ Download options (CSV, JSON, PDF)
✅ Real-time cheque count in profile
✅ Session state management
✅ Cross-page data persistence

## 📝 Post-Deployment Checklist

- [ ] Test MongoDB connection
- [ ] Verify Google Gemini API quota
- [ ] Test cheque extraction
- [ ] Verify data saves to database
- [ ] Check user profile updates
- [ ] Test download functionality
- [ ] Monitor error logs
- [ ] Set up database backups

## 🆘 Troubleshooting

### MongoDB Connection Issues
- Verify MONGO_URI is correct
- Check IP whitelist in MongoDB Atlas
- Ensure certifi and dnspython are installed
- Test connection: `client.admin.command('ping')`

### Gemini API Errors
- Check API key is valid
- Monitor rate limits (5 requests/minute free tier)
- Upgrade to paid plan if needed

### Deployment Errors
- Check all dependencies in requirements.txt
- Verify Python version (3.8+)
- Check Streamlit Cloud logs
- Ensure secrets are properly set

## 📞 Support
For issues, check the error logs in Streamlit Cloud dashboard or MongoDB Atlas monitoring.
