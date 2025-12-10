"""
Debug script to see exactly what's in MongoDB for each user
"""

from dotenv import load_dotenv
import os
import pymongo

def get_mongodb_client():
    try:
        load_dotenv(override=True)
        MONGO_URI = os.getenv("MONGO_URI")
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
        print(f"ERROR: {e}")
        return None

client = get_mongodb_client()
if client:
    db = client['checkmate_db']
    collection = db['user_profiles']
    
    print("\n" + "="*80)
    print("ALL USER DATA IN MONGODB")
    print("="*80 + "\n")
    
    users = collection.find({})
    for i, user in enumerate(users, 1):
        print(f"{i}. Username: {user.get('username', 'MISSING')}")
        print(f"   Fields: {list(user.keys())}")
        print(f"   Has password_hash: {'password_hash' in user}")
        print(f"   Has name: {'name' in user}")
        print(f"   Has email: {'email' in user}")
        if 'name' in user:
            print(f"   Name value: {user['name']}")
        print()
    
    client.close()
