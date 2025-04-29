from datetime import datetime
from bson import ObjectId


class Message:
    """
    Represents a message (artwork share) in the chat.

    Fields:
    - user_id: ID of the user who sent the message
    - artwork_id: ID of the artwork that was shared
    - timestamp: When the message was sent
    - seen_by: List of user IDs who have seen this message
    """

    collection_name = 'messages'

    @staticmethod
    def get_collection(db):
        """Get the MongoDB collection for messages"""
        return db[Message.collection_name]

    @staticmethod
    def find_one(db, message_id):
        """Find a message by ID"""
        return Message.get_collection(db).find_one({'_id': ObjectId(message_id)})

    @staticmethod
    def find_recent(db, limit=50):
        """Get recent messages, with newest first"""
        return list(Message.get_collection(db).find().sort('timestamp', -1).limit(limit))

    @staticmethod
    def create(db, user_id, artwork_id):
        """Create a new message"""
        message = {
            'user_id': ObjectId(user_id),
            'artwork_id': ObjectId(artwork_id),
            'timestamp': datetime.utcnow(),
            'seen_by': [ObjectId(user_id)]  # Sender has seen it
        }

        result = Message.get_collection(db).insert_one(message)
        message['_id'] = result.inserted_id
        return message

    @staticmethod
    def mark_seen(db, message_id, user_id):
        """Mark a message as seen by a user"""
        try:
            Message.get_collection(db).update_one(
                {'_id': ObjectId(message_id)},
                {'$addToSet': {'seen_by': ObjectId(user_id)}}
            )
        except Exception as e:
            print(f"Error in mark_seen: {str(e)}")

    @staticmethod
    def get_with_details(db, message_id):
        """Get a message with user and artwork details"""
        # Using MongoDB aggregation pipeline to join collections
        pipeline = [
            {'$match': {'_id': ObjectId(message_id)}},
            {'$lookup': {
                'from': 'users',
                'localField': 'user_id',
                'foreignField': '_id',
                'as': 'user'
            }},
            {'$lookup': {
                'from': 'artworks',
                'localField': 'artwork_id',
                'foreignField': '_id',
                'as': 'artwork'
            }},
            {'$unwind': '$user'},
            {'$unwind': '$artwork'},
            {'$project': {
                'timestamp': 1,
                'seen_by': 1,
                'user': {
                    '_id': 1,
                    'username': 1,
                    'display_name': 1,
                    'avatar': 1
                },
                'artwork': {
                    '_id': 1,
                    'title': 1,
                    'file_path': 1
                }
            }}
        ]

        result = list(Message.get_collection(db).aggregate(pipeline))
        return result[0] if result else None
