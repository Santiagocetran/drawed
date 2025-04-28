import pytest
from bson import ObjectId
from werkzeug.security import check_password_hash

from app.models.user import User


def test_user_creation(db):
    """Test creating a new user."""
    user = User.create(
        db,
        username="johndoe",
        email="john@example.com",
        password="securepassword",
        display_name="John Doe"
    )

    # Check that user was created with all fields
    assert user is not None
    assert isinstance(user["_id"], ObjectId)
    assert user["username"] == "johndoe"
    assert user["email"] == "john@example.com"
    assert user["display_name"] == "John Doe"
    assert "password_hash" in user
    # Password should be hashed, not stored in plain text
    assert user["password_hash"] != "securepassword"


def test_find_user(db, test_user):
    """Test finding a user by ID."""
    user = User.find_one(db, test_user["_id"])

    assert user is not None
    assert user["username"] == test_user["username"]
    assert user["email"] == test_user["email"]


def test_find_by_username(db, test_user):
    """Test finding a user by username."""
    user = User.find_by_username(db, test_user["username"])

    assert user is not None
    assert user["_id"] == test_user["_id"]
    assert user["email"] == test_user["email"]


def test_find_by_email(db, test_user):
    """Test finding a user by email."""
    user = User.find_by_email(db, test_user["email"])

    assert user is not None
    assert user["_id"] == test_user["_id"]
    assert user["username"] == test_user["username"]


def test_password_verification(db, test_user):
    """Test password verification."""
    # Correct password
    assert User.verify_password(
        db, test_user["username"], "password123") is True

    # Incorrect password
    assert User.verify_password(
        db, test_user["username"], "wrongpassword") is False


def test_duplicate_username(db, test_user):
    """Test that creating a user with a duplicate username raises an error."""
    with pytest.raises(ValueError):
        User.create(
            db,
            username=test_user["username"],  # Same username as test_user
            email="another@example.com",
            password="password123"
        )


def test_update_last_active(db, test_user):
    """Test updating a user's last_active timestamp."""
    # Get original last_active
    original_user = User.find_one(db, test_user["_id"])
    original_timestamp = original_user["last_active"]

    # Wait a moment to ensure timestamp will be different
    import time
    time.sleep(0.1)

    # Update last_active
    User.update_last_active(db, test_user["_id"])

    # Check that last_active was updated
    updated_user = User.find_one(db, test_user["_id"])
    assert updated_user["last_active"] > original_timestamp
