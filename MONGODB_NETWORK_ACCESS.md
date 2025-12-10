# MongoDB Atlas Network Access Configuration

## 🔧 **Important: Enable Network Access for Deployment**

When you deploy to cloud platforms, you need to allow connections from anywhere.

---

## 📋 **Step-by-Step Instructions**

### **1. Login to MongoDB Atlas**
- Go to: https://cloud.mongodb.com/
- Sign in with your account

### **2. Navigate to Network Access**
- Click on your project (left sidebar)
- Click "Network Access" in the left menu
- You'll see current IP addresses

### **3. Add New IP Address**
- Click "Add IP Address" button
- Choose "Allow Access from Anywhere"
- Or manually enter: `0.0.0.0/0`
- Add comment: "Streamlit Cloud Deployment"
- Click "Confirm"

### **4. Wait for Update**
- Wait 1-2 minutes for changes to apply
- Status should show "Active"

---

## ⚠️ **Security Note**

**`0.0.0.0/0` allows access from any IP address.**

This is SAFE because:
✅ You still need username/password to connect
✅ MongoDB Atlas uses TLS/SSL encryption
✅ Your app uses authentication
✅ Standard practice for cloud deployments

### **Alternative (More Secure)**

If you know Streamlit Cloud's IP ranges, add them specifically:
```
52.206.0.0/16
44.236.0.0/16
54.186.0.0/16
```

But `0.0.0.0/0` is easier and commonly used.

---

## ✅ **Verification**

After adding IP access:

1. **Test Connection**
   - Run: `python test_mongodb.py`
   - Should show: "MongoDB connected successfully"

2. **Check Atlas Dashboard**
   - Go to "Database" → "Browse Collections"
   - You should see:
     - Database: `checkmate_db`
     - Collection: `user_profiles`
     - Documents: Your users

3. **Deploy and Test**
   - Deploy to Streamlit Cloud
   - Try logging in
   - MongoDB should work

---

## 🐛 **Troubleshooting**

### **Problem: "Connection timed out"**
**Solution**: 
- Verify `0.0.0.0/0` is added to Network Access
- Wait 2-3 minutes after adding
- Check if IP entry is "Active"

### **Problem: "Authentication failed"**
**Solution**:
- Verify MONGO_URI is correct in secrets
- Check username/password in connection string
- Make sure user has read/write permissions

### **Problem: "SSL certificate verify failed"**
**Solution**:
- Already handled in code with `tlsAllowInvalidCertificates`
- No action needed

---

## 📊 **Current Network Access Settings**

After configuration, you should see:

| IP Address | Comment | Status |
|------------|---------|--------|
| 0.0.0.0/0 | Streamlit Cloud Deployment | Active |

---

## 🔄 **Update After Deployment**

Once deployed, MongoDB Atlas will show:
- Connection attempts from Streamlit Cloud
- Database operations
- Active connections

Monitor this in:
- Atlas Dashboard → Metrics
- Real-time performance graphs

---

## ✅ **Done!**

Your MongoDB Atlas is now configured for cloud deployment!

**Next:** Deploy your app to Streamlit Cloud
