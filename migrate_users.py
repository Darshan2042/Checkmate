"""
Migration script to add default passwords for existing users in MongoDB
This allows existing users (who were created before password storage was implemented) to log in
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
        print("✓ MongoDB connected successfully")
        return client
        
    except Exception as e:
        print(f"ERROR: MongoDB connection failed: {str(e)}")
        return None

def migrate_existing_users():
    """Add default passwords to existing users who don't have password_hash"""
    client = get_mongodb_client()
    if not client:
        return
    
    try:
        db = client['checkmate_db']
        collection = db['user_profiles']
        
        # Find all users
        all_users = list(collection.find({}))
        print(f"\n{'='*80}")
        print(f"Found {len(all_users)} users in database")
        print(f"{'='*80}\n")
        
        users_without_password = []
        users_with_password = []
        
        for user in all_users:
            username = user.get('username', 'unknown')
            if 'password_hash' not in user or not user['password_hash']:
                users_without_password.append(username)
            else:
                users_with_password.append(username)
        
        print(f"Users WITH passwords: {len(users_with_password)}")
        for username in users_with_password:
            print(f"  ✓ {username}")
        
        print(f"\nUsers WITHOUT passwords: {len(users_without_password)}")
        for username in users_without_password:
            print(f"  ✗ {username}")
        
        if not users_without_password:
            print("\n✓ All users already have passwords!")
            return
        
        print(f"\n{'='*80}")
        print("MIGRATION OPTIONS")
        print(f"{'='*80}")
        print("\nChoose how to set passwords for users without passwords:")
        print("1. Set default password 'password123' for all")
        print("2. Set password same as username (e.g., user 'john' → password 'john')")
        print("3. Cancel migration")
        
        choice = input("\nEnter your choice (1/2/3): ").strip()
        
        if choice == '3':
            print("\n✗ Migration cancelled")
            return
        
        if choice not in ['1', '2']:
            print("\n✗ Invalid choice")
            return
        
        print(f"\n{'='*80}")
        print("MIGRATING USERS")
        print(f"{'='*80}\n")
        
        migrated_count = 0
        
        for username in users_without_password:
            try:
                # Determine password based on choice
                if choice == '1':
                    password = 'password123'
                else:  # choice == '2'
                    password = username
                
                # Hash the password
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                hashed_password_str = hashed_password.decode()
                
                # Update user with password
                result = collection.update_one(
                    {'username': username},
                    {'$set': {
                        'password_hash': hashed_password_str,
                        'last_updated': datetime.now().isoformat()
                    }}
                )
                
                if result.modified_count > 0:
                    print(f"✓ Migrated user: {username} (password: {password})")
                    migrated_count += 1
                else:
                    print(f"✗ Failed to migrate: {username}")
                    
            except Exception as e:
                print(f"✗ Error migrating {username}: {str(e)}")
        
        print(f"\n{'='*80}")
        print(f"MIGRATION COMPLETE")
        print(f"{'='*80}")
        print(f"Successfully migrated: {migrated_count}/{len(users_without_password)} users")
        
        if choice == '1':
            print(f"\n⚠️  All migrated users can now login with password: password123")
        else:
            print(f"\n⚠️  All migrated users can now login with password: <their username>")
        
        print("\n💡 Users should change their passwords after first login!")
        
    except Exception as e:
        print(f"ERROR during migration: {str(e)}")
        import traceback
        print(traceback.format_exc())
    finally:
        if client:
            client.close()

if __name__ == "__main__":
    print("\n" + "="*80)
    print("USER PASSWORD MIGRATION SCRIPT")
    print("="*80)
    print("\nThis script will add passwords to existing users in MongoDB")
    print("who don't have password_hash field.\n")
    
    migrate_existing_users()
    
    print("\n" + "="*80)
    print("MIGRATION SCRIPT FINISHED")
    print("="*80 + "\n")
