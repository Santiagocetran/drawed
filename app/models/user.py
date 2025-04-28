from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId

class User:
    """
    Represents a user in the system.
    
    Fields:
    - username: Unique username
    - email: User's email address
    - password_hash: Hashed password
    - display_name: Name shown in chat
    - avatar: Path to user's avatar image (optional)
    - last_active: Timestamp of last activity
    - created_at: When the account was created
    """
    
    collection_name = 'users'
    
    @staticmethod
    def get_collection(db):
        """Get the MongoDB collection for users"""
        return db[User.collection_name]
    
    @staticmethod
    def find_one(db, user_id):
        """Find a user by ID"""
        return User.get_collection(db).find_one({'_id': ObjectId(user_id)})
    
    @staticmethod
    def find_by_username(db, username):
        """Find a user by username"""
        return User.get_collection(db).find_one({'username': username})
    
    @staticmethod
    def find_by_email(db, email):
        """Find a user by email"""
        return User.get_collection(db).find_one({'email': email})
    
    @staticmethod
    def create(db, username, email, password, display_name=None):
        """Create a new user"""
        # Check if username or email already exists
        if User.find_by_username(db, username):
            raise ValueError(f"Username '{username}' is already taken")
        
        if User.find_by_email(db, email):
            raise ValueError(f"Email '{email}' is already registered")
        
        # Create new user document
        user = {
            'username': username,
            'email': email,
            'password_hash': generate_password_hash(password),
            'display_name': display_name or username,
            'avatar': None,
            'last_active': datetime.utcnow(),
            'created_at': datetime.utcnow()
        }
        
        result = User.get_collection(db).insert_one(user)
        user['_id'] = result.inserted_id
        return user
    
    @staticmethod
    def verify_password(db, username, password):
        """Verify a user's password"""
        user = User.find_by_username(db, username)
        if not user:
            return False
        return check_password_hash(user['password_hash'], password)
    
    @staticmethod
    def update_last_active(db, user_id):
        """Update a user's last_active timestamp"""
        User.get_collection(db).update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'last_active': datetime.utcnow()}}
        )