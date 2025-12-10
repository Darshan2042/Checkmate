"""
Test MongoDB Connection
Run this to verify your MongoDB Atlas connection is working
"""
import os
from dotenv import load_dotenv
import pymongo

def test_mongodb_connection():
    print("=" * 60)
    print("Testing MongoDB Atlas Connection")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv(override=True)
    MONGO_URI = os.getenv("MONGO_URI")
    
    if not MONGO_URI:
        print("❌ ERROR: MONGO_URI not found in .env file")
        return False
    
    # Clean the URI
    MONGO_URI = MONGO_URI.strip('"').strip("'").strip().replace('\n', '').replace('\r', '')
    
    print(f"\n📋 Connection String (first 50 chars): {MONGO_URI[:50]}...")
    print(f"📋 Connection String length: {len(MONGO_URI)} characters\n")
    
    try:
        print("🔄 Attempting to connect to MongoDB Atlas...")
        
        # Try to connect
        client = pymongo.MongoClient(
            MONGO_URI,
            tls=True,
            tlsAllowInvalidCertificates=True,
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=10000
        )
        
        # Test connection
        print("🔄 Testing connection with ping command...")
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB Atlas!")
        
        # Get database
        db = client['checkmate_db']
        print(f"\n✅ Database 'checkmate_db' accessible")
        
        # Test writing to user_profiles collection
        print("\n🔄 Testing write to 'user_profiles' collection...")
        profiles_collection = db['user_profiles']
        
        test_profile = {
            'username': 'test_user_' + str(os.urandom(4).hex()),
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '+1 555 0000',
            'role': 'Test',
            'bio': 'Test profile',
            'joined_date': 'Dec 2024',
            'total_cheques': 0
        }
        
        result = profiles_collection.insert_one(test_profile)
        print(f"✅ Successfully wrote test document with ID: {result.inserted_id}")
        
        # Read it back
        print("\n🔄 Reading back the test document...")
        found_profile = profiles_collection.find_one({'_id': result.inserted_id})
        if found_profile:
            print(f"✅ Successfully read back: {found_profile['username']}")
        
        # Clean up test document
        print("\n🔄 Cleaning up test document...")
        profiles_collection.delete_one({'_id': result.inserted_id})
        print("✅ Test document deleted")
        
        # List all collections
        print("\n📊 Existing collections in 'checkmate_db':")
        collections = db.list_collection_names()
        if collections:
            for col in collections:
                count = db[col].count_documents({})
                print(f"  - {col}: {count} documents")
        else:
            print("  (No collections yet)")
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED! MongoDB is working correctly!")
        print("=" * 60)
        
        client.close()
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        print("\nFull error details:")
        print(traceback.format_exc())
        print("\n" + "=" * 60)
        print("❌ CONNECTION FAILED")
        print("=" * 60)
        return False

if __name__ == "__main__":
    test_mongodb_connection()
