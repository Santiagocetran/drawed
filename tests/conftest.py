from app.models.message import Message
from app.models.artwork import Artwork
from app.models.user import User
from app.database import get_db
from app import create_app
import pytest
import os
import sys
from datetime import datetime
from bson import ObjectId

# Add project root to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    app = create_app('testing')

    # Create a test context
    with app.app_context():
        yield app

        # Clean up / reset resources
        db = get_db()
        db.users.delete_many({})
        db.artworks.delete_many({})
        db.messages.delete_many({})


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def db(app):
    """Get the database connection."""
    with app.app_context():
        db = get_db()
        yield db


@pytest.fixture
def test_user(db):
    """Create a test user."""
    user = User.create(
        db,
        username="testuser",
        email="test@example.com",
        password="password123",
        display_name="Test User"
    )
    return user


@pytest.fixture
def test_artwork(db):
    """Create a test artwork."""
    artwork = Artwork.create(
        db,
        title="Test Artwork",
        artist="Test Artist",
        period="Test Period",
        year=2023,
        file_path="/artworks/test.jpg",
        metadata={"description": "A test artwork."}
    )
    return artwork


@pytest.fixture
def test_message(db, test_user, test_artwork):
    """Create a test message."""
    message = Message.create(
        db,
        user_id=test_user["_id"],
        artwork_id=test_artwork["_id"]
    )
    return message
