"""
View all users in MongoDB
"""
import os
from dotenv import load_dotenv
import pymongo

load_dotenv(override=True)
MONGO_URI = os.getenv("MONGO_URI")
MONGO_URI = MONGO_URI.strip('"').strip("'").strip().replace('\n', '').replace('\r', '')

client = pymongo.MongoClient(
    MONGO_URI,
    tls=True,
    tlsAllowInvalidCertificates=True,
    serverSelectionTimeoutMS=10000
)

db = client['checkmate_db']
profiles = db['user_profiles']

print("\n" + "="*80)
print("ALL USERS IN MONGODB")
print("="*80)

all_users = list(profiles.find({}))

if not all_users:
    print("\n❌ No users found in database")
else:
    print(f"\n✅ Found {len(all_users)} users:\n")
    for i, user in enumerate(all_users, 1):
        print(f"{i}. Username: {user.get('username', 'N/A')}")
        print(f"   Name: {user.get('name', 'N/A')}")
        print(f"   Email: {user.get('email', 'N/A')}")
        print(f"   Phone: {user.get('phone', 'N/A')}")
        print(f"   Role: {user.get('role', 'N/A')}")
        print(f"   Joined: {user.get('joined_date', 'N/A')}")
        print(f"   Total Cheques: {user.get('total_cheques', 0)}")
        print(f"   Last Updated: {user.get('last_updated', 'N/A')}")
        print(f"   Has Photo: {'Yes' if user.get('photo') else 'No'}")
        print()

print("="*80)

# Check for cheque collections
print("\nCHEQUE COLLECTIONS:")
print("="*80)
collections = [col for col in db.list_collection_names() if col.startswith('cheques_')]
if collections:
    for col in collections:
        count = db[col].count_documents({})
        username = col.replace('cheques_', '')
        print(f"  - {username}: {count} cheques")
else:
    print("  No cheque collections yet")

print("\n" + "="*80)

client.close()
