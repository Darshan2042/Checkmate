# Testing Guide - User Data Isolation

## ✅ **What Was Fixed**

### **Problem:**
When users extracted cheque data, it wasn't being properly linked to their account because:
1. Profile data wasn't loaded from MongoDB during login/signup
2. Empty profile data was used when saving cheque extractions
3. User data appeared to "reset" when switching accounts

### **Solution:**
1. ✅ Profile data now loads from MongoDB immediately after login/signup
2. ✅ New users get a profile created and saved to MongoDB automatically
3. ✅ Cheque extraction checks for profile data and loads it if missing
4. ✅ All cheque data includes proper user information (name, email, phone)

## 🧪 **Testing Steps**

### **Test 1: New User Registration**

1. **Sign Up** with a new username (e.g., `user1`)
2. ✅ **Expected**: Profile automatically created and saved to MongoDB
3. Go to **Profile Page**
4. ✅ **Expected**: Should see default profile:
   - Name: User1
   - Email: user1@checkmate.ai
   - Phone: +1 (555) 000-0000
   - Cheque Count: 0

### **Test 2: First Cheque Extraction**

1. Login as `user1`
2. Go to **Home Page**
3. Upload a cheque image
4. ✅ **Expected**: Cheque extracted and saved with user info:
   ```json
   {
     "Bank Name": "...",
     "username": "user1",
     "extracted_by": "User1",
     "user_email": "user1@checkmate.ai",
     "user_phone": "+1 (555) 000-0000"
   }
   ```
5. Check **Profile Page**
6. ✅ **Expected**: Cheque count = 1

### **Test 3: Profile Update**

1. Login as `user1`
2. Go to **Profile Page**
3. Click **Edit Profile**
4. Update:
   - Name: "John Smith"
   - Email: "john@example.com"
   - Phone: "+1 555-1234"
5. Click **Save Changes**
6. ✅ **Expected**: "Profile updated and saved to database!" message
7. Logout and login again as `user1`
8. ✅ **Expected**: Profile shows updated information

### **Test 4: Multiple Cheque Extractions**

1. Login as `user1`
2. Extract 3 different cheques
3. ✅ **Expected**: Each cheque saved with user1's updated profile info
4. Check **Profile Page**
5. ✅ **Expected**: Cheque count = 4 (1 from Test 2 + 3 new)

### **Test 5: Second User - Data Isolation**

1. **Logout** from user1
2. **Sign Up** with username `user2`
3. ✅ **Expected**: Fresh profile created for user2
4. Go to **Profile Page**
5. ✅ **Expected**: 
   - Name: User2
   - Cheque Count: 0 (NOT user1's count!)
6. Extract 2 cheques
7. ✅ **Expected**: Cheques saved to `cheques_user2` collection
8. Check **Profile Page**
9. ✅ **Expected**: Cheque count = 2

### **Test 6: Switching Between Users**

1. Logout from `user2`
2. Login as `user1`
3. Go to **Profile Page**
4. ✅ **Expected**: 
   - Shows user1's profile (John Smith, john@example.com)
   - Cheque count = 4
5. Logout and login as `user2`
6. ✅ **Expected**:
   - Shows user2's profile
   - Cheque count = 2

### **Test 7: Data Persistence**

1. Login as `user1`
2. Extract a cheque
3. Navigate to **Profile Page**
4. Navigate back to **Home Page**
5. ✅ **Expected**: Last extracted cheque still visible
6. Logout
7. Login as `user1` again
8. Go to **Home Page**
9. ✅ **Expected**: Can click "Extract New Cheque" (previous data cleared on logout)
10. Go to **Profile Page**
11. ✅ **Expected**: Cheque count shows all user1's cheques (5 total now)

## 📊 **MongoDB Verification**

### **Check User Profiles:**
```javascript
use checkmate_db
db.user_profiles.find({}).pretty()
```

✅ **Expected Output:**
```json
[
  {
    "username": "user1",
    "name": "John Smith",
    "email": "john@example.com",
    "phone": "+1 555-1234",
    "role": "Premium User",
    "bio": "AI-powered cheque processing user",
    "joined_date": "Dec 2024",
    "last_updated": "2024-12-09T..."
  },
  {
    "username": "user2",
    "name": "User2",
    "email": "user2@checkmate.ai",
    "phone": "+1 (555) 000-0000",
    ...
  }
]
```

### **Check User1's Cheques:**
```javascript
db.cheques_user1.find({}).pretty()
```

✅ **Expected**: Should show 5 cheques, all with:
- `username: "user1"`
- `extracted_by: "John Smith"`
- `user_email: "john@example.com"`

### **Check User2's Cheques:**
```javascript
db.cheques_user2.find({}).pretty()
```

✅ **Expected**: Should show 2 cheques, all with:
- `username: "user2"`
- User2's profile information

### **Verify Data Isolation:**
```javascript
// User1 should NOT see user2's cheques
db.cheques_user1.find({ username: "user2" }).count()
// Should return: 0

// User2 should NOT see user1's cheques
db.cheques_user2.find({ username: "user1" }).count()
// Should return: 0
```

## 🎯 **What to Look For**

### ✅ **Success Indicators:**
- Each user sees only their own data
- Profile changes persist across sessions
- Cheque count matches actual extractions
- MongoDB collections are user-specific (`cheques_user1`, `cheques_user2`)
- Profile data automatically loads on login
- New users get profiles created automatically

### ❌ **Failure Indicators:**
- Users see other users' cheque counts
- Profile data resets to default on login
- Cheques saved with empty/wrong user info
- MongoDB shows wrong username in cheque documents
- Profile updates don't save to database

## 🔍 **Debug Checks**

If something doesn't work:

1. **Check Browser Console** (F12):
   - Look for JavaScript errors
   - Check network requests

2. **Check Streamlit Logs**:
   ```powershell
   # In terminal where streamlit is running
   # Look for error messages
   ```

3. **Check MongoDB Connection**:
   - Verify `.env` file has correct `MONGO_URI`
   - Test connection with `mongosh`

4. **Check Session State**:
   - Add debug print in code:
   ```python
   st.write("Session State:", st.session_state)
   ```

5. **Verify Profile Loading**:
   - In `authentication.py`, check if `initialize_user_profile()` is called
   - In `cheque_extractor.py`, check if profile loads before saving

## 📝 **Summary of Changes**

### **Files Modified:**

1. **authentication.py**
   - Added `initialize_user_profile()` function
   - Calls it after login (line ~230)
   - Calls it after signup (line ~30)

2. **cheque_extractor.py**
   - Added profile check before saving cheques (line ~495)
   - Loads profile from MongoDB if not in session
   - Creates default profile if none exists

3. **user_profile.py**
   - Loads profile from MongoDB on page load
   - Detects user switching via `current_profile_user`
   - Auto-saves profile changes to MongoDB

### **How It Works:**

```
1. User Login/Signup
   ↓
2. initialize_user_profile() called
   ↓
3. Load from MongoDB OR create new profile
   ↓
4. Save to st.session_state.profile_data
   ↓
5. User extracts cheque
   ↓
6. Check if profile_data exists (if not, load it)
   ↓
7. Save cheque with user info to cheques_{username}
   ↓
8. Profile page shows correct count
```

## 🚀 **Ready for Production**

After testing, your application is ready to deploy with:
- ✅ Multi-user support
- ✅ Data isolation per user
- ✅ Profile persistence
- ✅ MongoDB integration
- ✅ Automatic profile initialization
