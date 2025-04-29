from datetime import datetime
from bson import ObjectId


class Artwork:
    """
    Represents an artwork in the database.

    Fields:
    - title: Name of the artwork
    - file_path: Path to the artwork image file
    - created_at: When this record was created
    """

    collection_name = 'artworks'

    @staticmethod
    def get_collection(db):
        """Get the MongoDB collection for artworks"""
        return db[Artwork.collection_name]

    @staticmethod
    def find_one(db, artwork_id):
        """Find an artwork by its ID"""
        return Artwork.get_collection(db).find_one({'_id': ObjectId(artwork_id)})

    @staticmethod
    def find_all(db, limit=100):
        """Get all artworks, with optional limit"""
        return list(Artwork.get_collection(db).find().limit(limit))

    @staticmethod
    def random(db):
        """Get a random artwork from the database"""
        # MongoDB aggregation pipeline to get a random document
        pipeline = [{'$sample': {'size': 1}}]
        result = list(Artwork.get_collection(db).aggregate(pipeline))
        return result[0] if result else None

    @staticmethod
    def create(db, title, file_path):
        """Create a new artwork record"""
        artwork = {
            'title': title,
            'file_path': file_path,
            'created_at': datetime.utcnow()
        }

        result = Artwork.get_collection(db).insert_one(artwork)
        artwork['_id'] = result.inserted_id
        return artwork
