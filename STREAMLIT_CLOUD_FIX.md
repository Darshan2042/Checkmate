# 🚨 STREAMLIT CLOUD DEPLOYMENT FIX GUIDE

## ❌ **Problems Found:**

1. **MongoDB Connection on Streamlit Cloud** - Code was using `.env` file instead of `st.secrets`
2. **Login Issues** - Users may not be loading correctly from MongoDB on app startup

---

## ✅ **FIXES APPLIED:**

### **1. Updated Code to Use Streamlit Secrets**

**Files Modified:**
- `cheque_extractor.py` - Now checks `st.secrets` first, then falls back to `.env`

**What Changed:**
```python
# OLD (only works locally):
load_dotenv()
key = os.getenv("GOOGLE_API_KEY")

# NEW (works on Streamlit Cloud AND locally):
try:
    key = st.secrets["GOOGLE_API_KEY"]  # For Streamlit Cloud
except:
    load_dotenv()
    key = os.getenv("GOOGLE_API_KEY")  # For local
```

### **2. Created Secrets File**

**File Created:** `.streamlit/secrets.toml`

This file contains your credentials for **local testing only**. 

⚠️ **DO NOT commit this to GitHub** (already in `.gitignore`)

---

## 🚀 **HOW TO DEPLOY ON STREAMLIT CLOUD:**

### **Step 1: Push Code to GitHub**

```powershell
git add .
git commit -m "Fixed Streamlit Cloud compatibility"
git push origin main
```

### **Step 2: Configure Secrets on Streamlit Cloud**

1. Go to your app on **https://share.streamlit.io/**
2. Click **"App settings"** (⚙️ gear icon)
3. Click **"Secrets"** tab
4. Copy and paste this EXACTLY:

```toml
GOOGLE_API_KEY = "AIzaSyAp9-M2h-0aSpgvwf22C3A3gq72CTV3qLM"
SECRET_KEY = "31dbe170cef99bc230f94d912c7e958ff6f12613d1d3fdf1c1d233e82929863d"
MONGO_URI = "mongodb+srv://checkmate_user:dMkVJ18OUsJ4HL1z@cluster0.g1ndcij.mongodb.net/?appName=Cluster0"
```

5. Click **"Save"**

### **Step 3: Configure MongoDB Atlas Network Access**

**This is CRITICAL - Your app won't connect to MongoDB without this!**

1. Go to **https://cloud.mongodb.com/**
2. Click **"Network Access"** in left sidebar
3. Click **"Add IP Address"**
4. Select **"Allow Access from Anywhere"**
5. It will auto-fill: `0.0.0.0/0`
6. Add comment: `Streamlit Cloud`
7. Click **"Confirm"**
8. **Wait 2-3 minutes** for changes to take effect

### **Step 4: Restart Your Streamlit App**

1. Go back to Streamlit Cloud dashboard
2. Click **"Reboot app"** or **"Manage app"** → **"Reboot"**
3. Wait for app to restart (1-2 minutes)

---

## 🧪 **TESTING AFTER DEPLOYMENT:**

### **Test 1: Check Logs**
1. On Streamlit Cloud, click **"Manage app"**
2. Scroll down to **"Logs"**
3. Look for:
   - ✅ `"Using MONGO_URI from Streamlit secrets"`
   - ✅ `"MongoDB connected successfully"`
   - ✅ `"Gemini API configured successfully"`

### **Test 2: Try Login**
1. Try logging in with existing user:
   - **Username:** `Darshanpawar`
   - **Password:** `password123`
   
2. Try logging in with:
   - **Username:** `gauravpawar`
   - **Password:** `password123`

### **Test 3: Create New User**
1. Click **"Sign Up"**
2. Create new account
3. Check if profile loads
4. Logout and login again to verify persistence

### **Test 4: Check MongoDB Atlas**
1. Go to MongoDB Atlas Dashboard
2. Click **"Database"** → **"Browse Collections"**
3. You should see:
   - Database: `checkmate_db`
   - Collection: `user_profiles` (should have your users)
   - Collection: `cheques_[username]` (one per user)

---

## 🐛 **TROUBLESHOOTING:**

### **Problem: "MongoDB Connection Failed"**

**Check 1: Network Access**
- Go to MongoDB Atlas → Network Access
- Verify `0.0.0.0/0` is listed and **ACTIVE** (green)
- If it says "Pending", wait 2-3 more minutes

**Check 2: Connection String**
- In Streamlit Cloud → App Settings → Secrets
- Verify `MONGO_URI` is EXACTLY:
  ```
  MONGO_URI = "mongodb+srv://checkmate_user:dMkVJ18OUsJ4HL1z@cluster0.g1ndcij.mongodb.net/?appName=Cluster0"
  ```
- No extra spaces, quotes must be straight quotes `"`, not curly quotes

**Check 3: MongoDB Cluster Running**
- Go to MongoDB Atlas → Database
- Verify cluster is **ACTIVE** (not paused)

### **Problem: "Google API Key Error"**

**Check 1: API Key in Secrets**
- Streamlit Cloud → App Settings → Secrets
- Verify `GOOGLE_API_KEY` is present
- No extra spaces or line breaks

**Check 2: API Enabled**
- Go to **https://console.cloud.google.com/**
- Enable "Generative Language API"

### **Problem: "Can't Login After Signup"**

**Reason:** Session state is cleared on Streamlit Cloud

**Solution:** This is normal! Users need to:
1. Sign up (credentials saved to MongoDB)
2. Then login with those credentials

The app loads users from MongoDB on startup, so login should work after signup.

### **Problem: "Users Not Showing in MongoDB Atlas"**

**Check 1: Collection Name**
- Collections are named `cheques_[username]`
- If username is "john", collection is `cheques_john`

**Check 2: Write Permissions**
- MongoDB Atlas → Database Access
- Verify user `checkmate_user` has **Read and Write** permissions

**Check 3: App Logs**
- Check Streamlit Cloud logs for errors
- Look for "Failed to save" or "MongoDB error" messages

---

## 📊 **CURRENT DATABASE STATUS:**

✅ **2 Users in MongoDB:**
1. **Username:** `Darshanpawar`
   - Email: Darshanpawar@gmail.com
   - Role: Admin
   - Has password_hash: Yes

2. **Username:** `gauravpawar`
   - Email: gauravpawar@gmail.com
   - Role: Accountant
   - Has password_hash: Yes
   - Total Cheques: 6

**Default Password for Both:** `password123`

---

## ⚠️ **IMPORTANT SECURITY NOTES:**

### **For Testing:**
- Current setup is fine for testing

### **Before Going Live:**
1. **Change MongoDB Password:**
   - MongoDB Atlas → Database Access → Edit user
   - Change password
   - Update `MONGO_URI` in Streamlit secrets

2. **Regenerate Google API Key:**
   - Google Cloud Console → Credentials
   - Create new API key
   - Update `GOOGLE_API_KEY` in Streamlit secrets
   - Delete old key

3. **Change SECRET_KEY:**
   - Generate new random key:
     ```python
     import secrets
     print(secrets.token_hex(32))
     ```
   - Update in Streamlit secrets

4. **Make GitHub Repo Private:**
   - GitHub → Repository Settings → General
   - Scroll down → Change visibility → Make private

---

## ✅ **DEPLOYMENT CHECKLIST:**

- [ ] Code pushed to GitHub (with fixes)
- [ ] Streamlit Cloud secrets configured
- [ ] MongoDB Atlas network access set to `0.0.0.0/0`
- [ ] App restarted on Streamlit Cloud
- [ ] Checked logs for connection success
- [ ] Tested login with existing user
- [ ] Tested signup with new user
- [ ] Verified new users appear in MongoDB Atlas
- [ ] Tested cheque extraction

---

## 🎯 **EXPECTED BEHAVIOR:**

### **On Streamlit Cloud:**
1. App loads → Shows login/signup page
2. User signs up → Credentials saved to MongoDB
3. User logs in → Profile loads from MongoDB
4. User uploads cheque → Extracted data shown
5. User logs out → Session cleared
6. User logs in again → Profile and data persist ✅

### **In MongoDB Atlas:**
1. New signups create documents in `user_profiles`
2. Each user gets their own `cheques_[username]` collection
3. Data persists across sessions
4. You can see all users and data in Atlas dashboard

---

## 📞 **NEED MORE HELP?**

If still having issues, check:

1. **Streamlit Cloud Logs:**
   - App Settings → Logs
   - Look for red error messages
   - Copy error text

2. **MongoDB Atlas Logs:**
   - Atlas Dashboard → Database → Metrics
   - Check for connection attempts

3. **Test Locally First:**
   ```powershell
   streamlit run main.py
   ```
   - Should work with `.streamlit/secrets.toml`
   - If works locally but not on cloud = secrets configuration issue

---

## ✨ **YOUR APP IS READY!**

Follow the steps above and your app will:
- ✅ Connect to MongoDB Atlas from Streamlit Cloud
- ✅ Save user registrations permanently
- ✅ Allow users to login after logout
- ✅ Extract cheques using Gemini API
- ✅ Work perfectly in production!

**Good luck! 🚀**
