from app.models.artwork import Artwork
from app.database import get_db
from app import create_app
import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


# Create Flask app context
app = create_app('development')


def test_mongodb_connection():
    """Test connecting to MongoDB"""
    with app.app_context():
        db = get_db()
        print("Connected to MongoDB!")
        print(f"Available collections: {db.list_collection_names()}")

        # Test inserting a sample artwork
        artwork = Artwork.create(
            db,
            title="Starry Night",
            file_path="/artworks/starry_night.jpg"
        )

        print(f"Created artwork with ID: {artwork['_id']}")

        # Test retrieving the artwork
        retrieved = Artwork.find_one(db, artwork['_id'])
        print(f"Retrieved artwork: {retrieved['title']}")


if __name__ == "__main__":
    test_mongodb_connection()
