"""
Test script to verify login authentication works with MongoDB
"""

from dotenv import load_dotenv
import os
import pymongo
import bcrypt

def get_mongodb_client():
    """Get MongoDB client"""
    try:
        load_dotenv(override=True)
        MONGO_URI = os.getenv("MONGO_URI")
        
        if not MONGO_URI:
            print("ERROR: MONGO_URI not found in .env file")
            return None
        
        MONGO_URI = MONGO_URI.strip('"').strip("'").strip().replace('\n', '').replace('\r', '')
        
        client = pymongo.MongoClient(
            MONGO_URI,
            tls=True,
            tlsAllowInvalidCertificates=True,
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=10000
        )
        client.admin.command('ping')
        return client
        
    except Exception as e:
        print(f"ERROR: MongoDB connection failed: {str(e)}")
        return None

def test_login(username, password):
    """Test if login works for a user"""
    client = get_mongodb_client()
    if not client:
        return False
    
    try:
        db = client['checkmate_db']
        collection = db['user_profiles']
        
        # Find user
        user = collection.find_one({'username': username})
        
        if not user:
            print(f"✗ User '{username}' not found in database")
            return False
        
        if 'password_hash' not in user:
            print(f"✗ User '{username}' has no password hash")
            return False
        
        # Check password
        password_hash = user['password_hash']
        if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
            print(f"✓ Login successful for '{username}'")
            return True
        else:
            print(f"✗ Incorrect password for '{username}'")
            return False
            
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False
    finally:
        if client:
            client.close()

if __name__ == "__main__":
    print("\n" + "="*80)
    print("LOGIN AUTHENTICATION TEST")
    print("="*80 + "\n")
    
    # Test all migrated users with default password
    test_users = ['Darshan', 'harshal', 'gaurav', 'Vaibhav', 'salman']
    default_password = 'password123'
    
    print(f"Testing login for all users with password: '{default_password}'\n")
    
    success_count = 0
    for username in test_users:
        if test_login(username, default_password):
            success_count += 1
        print()
    
    print("="*80)
    print(f"RESULTS: {success_count}/{len(test_users)} successful logins")
    print("="*80 + "\n")
    
    if success_count == len(test_users):
        print("✅ All users can login successfully!")
        print("\n💡 You can now login to the Streamlit app with:")
        print("   - Any username: Darshan, harshal, gaurav, Vaibhav, salman")
        print("   - Password: password123")
    else:
        print("⚠️  Some users cannot login. Please check the migration.")
