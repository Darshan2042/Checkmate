"""
Test script to verify new user registration saves credentials correctly to MongoDB
"""

from dotenv import load_dotenv
import os
import pymongo
import bcrypt
from datetime import datetime

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

def simulate_registration(username, password):
    """Simulate the registration process"""
    client = get_mongodb_client()
    if not client:
        return False
    
    try:
        db = client['checkmate_db']
        collection = db['user_profiles']
        
        print(f"\n{'='*80}")
        print(f"SIMULATING REGISTRATION FOR: {username}")
        print(f"{'='*80}\n")
        
        # Check if user already exists
        existing_user = collection.find_one({'username': username})
        if existing_user:
            print(f"✗ User '{username}' already exists in database")
            if 'password_hash' in existing_user:
                print(f"  ✓ Has password_hash: Yes")
                # Test login
                if bcrypt.checkpw(password.encode('utf-8'), existing_user['password_hash'].encode('utf-8')):
                    print(f"  ✓ Password matches: Yes")
                else:
                    print(f"  ✗ Password matches: No")
            else:
                print(f"  ✗ Has password_hash: No")
            return False
        
        # Step 1: Hash password
        print("Step 1: Hashing password...")
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        hashed_password_str = hashed_password.decode()
        print(f"  ✓ Password hashed")
        
        # Step 2: Save credentials to MongoDB
        print("\nStep 2: Saving credentials to MongoDB...")
        result = collection.update_one(
            {'username': username},
            {'$set': {
                'username': username,
                'password_hash': hashed_password_str,
                'last_updated': datetime.now().isoformat()
            }},
            upsert=True
        )
        print(f"  ✓ Credentials saved (Matched: {result.matched_count}, Modified: {result.modified_count}, Upserted: {result.upserted_id})")
        
        # Step 3: Save profile data
        print("\nStep 3: Saving profile data...")
        
        # Load existing data to preserve password_hash
        existing_data = collection.find_one({'username': username})
        
        profile_data = {
            'name': username.capitalize(),
            'email': f'{username}@checkmate.ai',
            'phone': '+1 (555) 000-0000',
            'role': 'Premium User',
            'bio': 'AI-powered cheque processing user',
            'photo': None,
            'joined_date': 'Dec 2024',
            'total_cheques': 0,
            'username': username,
            'last_updated': datetime.now().isoformat()
        }
        
        # Preserve password_hash
        if existing_data and 'password_hash' in existing_data:
            profile_data['password_hash'] = existing_data['password_hash']
            print(f"  ✓ Preserved password_hash")
        
        result = collection.update_one(
            {'username': username},
            {'$set': profile_data},
            upsert=True
        )
        print(f"  ✓ Profile saved (Matched: {result.matched_count}, Modified: {result.modified_count})")
        
        # Step 4: Verify data
        print("\nStep 4: Verifying saved data...")
        saved_user = collection.find_one({'username': username})
        
        if not saved_user:
            print(f"  ✗ ERROR: User not found in database!")
            return False
        
        checks_passed = 0
        total_checks = 0
        
        # Check username
        total_checks += 1
        if saved_user.get('username') == username:
            print(f"  ✓ Username: {username}")
            checks_passed += 1
        else:
            print(f"  ✗ Username mismatch")
        
        # Check password_hash
        total_checks += 1
        if 'password_hash' in saved_user and saved_user['password_hash']:
            print(f"  ✓ Password hash: Present")
            checks_passed += 1
            
            # Verify password works
            total_checks += 1
            if bcrypt.checkpw(password.encode('utf-8'), saved_user['password_hash'].encode('utf-8')):
                print(f"  ✓ Password verification: Success")
                checks_passed += 1
            else:
                print(f"  ✗ Password verification: Failed")
        else:
            print(f"  ✗ Password hash: Missing!")
        
        # Check profile fields
        profile_fields = ['name', 'email', 'phone', 'role', 'bio']
        for field in profile_fields:
            total_checks += 1
            if field in saved_user:
                print(f"  ✓ {field.capitalize()}: {saved_user[field]}")
                checks_passed += 1
            else:
                print(f"  ✗ {field.capitalize()}: Missing")
        
        print(f"\n{'='*80}")
        print(f"VERIFICATION: {checks_passed}/{total_checks} checks passed")
        print(f"{'='*80}")
        
        if checks_passed == total_checks:
            print(f"\n✅ Registration successful! User '{username}' can now login with password: {password}")
            return True
        else:
            print(f"\n⚠️  Registration completed with issues. Some data may be missing.")
            return False
            
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False
    finally:
        if client:
            client.close()

if __name__ == "__main__":
    print("\n" + "="*80)
    print("REGISTRATION TEST SCRIPT")
    print("="*80)
    print("\nThis script simulates the user registration process")
    print("and verifies that credentials are saved correctly to MongoDB.\n")
    
    # Test with a new user
    test_username = input("Enter test username (or press Enter for 'testuser'): ").strip()
    if not test_username:
        test_username = 'testuser'
    
    test_password = input(f"Enter password for '{test_username}' (or press Enter for 'test123'): ").strip()
    if not test_password:
        test_password = 'test123'
    
    simulate_registration(test_username, test_password)
    
    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80 + "\n")
