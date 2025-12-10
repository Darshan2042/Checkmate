"""
Clear All Data from MongoDB
This will delete all users and cheque data from the database
WARNING: This action cannot be undone!
"""
import os
from dotenv import load_dotenv
import pymongo

def clear_all_data():
    print("\n" + "="*80)
    print("⚠️  WARNING: DATABASE CLEANUP")
    print("="*80)
    print("\nThis will DELETE ALL data from your MongoDB database:")
    print("  - All user profiles")
    print("  - All cheque collections")
    print("  - All extracted data")
    print("\n❗ This action CANNOT be undone!")
    print("="*80)
    
    confirmation = input("\nType 'DELETE ALL' to confirm: ")
    
    if confirmation != "DELETE ALL":
        print("\n❌ Operation cancelled. No data was deleted.")
        return
    
    print("\n🔄 Connecting to MongoDB...")
    
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
    
    # Get all collections
    collections = db.list_collection_names()
    
    print(f"\n📊 Found {len(collections)} collections")
    
    deleted_count = 0
    
    # Delete all documents from each collection
    for collection_name in collections:
        collection = db[collection_name]
        count = collection.count_documents({})
        
        if count > 0:
            print(f"\n🗑️  Deleting {count} documents from '{collection_name}'...")
            result = collection.delete_many({})
            deleted_count += result.deleted_count
            print(f"   ✅ Deleted {result.deleted_count} documents")
        else:
            print(f"\n   '{collection_name}' is already empty")
    
    # Optionally drop all collections to completely clean the database
    print("\n🗑️  Dropping all collections...")
    for collection_name in collections:
        db.drop_collection(collection_name)
        print(f"   ✅ Dropped collection '{collection_name}'")
    
    print("\n" + "="*80)
    print(f"✅ CLEANUP COMPLETE!")
    print(f"   Total documents deleted: {deleted_count}")
    print(f"   Collections dropped: {len(collections)}")
    print("="*80)
    print("\n✨ Your database is now clean and ready for fresh data!")
    print("   You can now create new users from scratch.\n")
    
    client.close()

if __name__ == "__main__":
    clear_all_data()
