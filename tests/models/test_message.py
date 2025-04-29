import pytest
from bson import ObjectId
from datetime import datetime

from app.models.message import Message


def test_message_creation(db, test_user, test_artwork):
    """Test creating a new message."""
    message = Message.create(
        db,
        user_id=test_user["_id"],
        artwork_id=test_artwork["_id"]
    )

    # Check that message was created with all fields
    assert message is not None
    assert isinstance(message["_id"], ObjectId)
    assert message["user_id"] == ObjectId(test_user["_id"])
    assert message["artwork_id"] == ObjectId(test_artwork["_id"])
    assert isinstance(message["timestamp"], datetime)
    assert "seen_by" in message
    # Sender should automatically be added to seen_by
    assert ObjectId(test_user["_id"]) in message["seen_by"]


def test_find_message(db, test_message):
    """Test finding a message by ID."""
    message = Message.find_one(db, test_message["_id"])

    assert message is not None
    assert message["user_id"] == test_message["user_id"]
    assert message["artwork_id"] == test_message["artwork_id"]

    # Compare timestamps with a tolerance for microsecond differences
    time_diff = abs(
        (message["timestamp"] - test_message["timestamp"]).total_seconds())
    assert time_diff < 0.1  # Allow for a small difference in timestamps


def test_find_recent_messages(db, test_user, test_artwork):
    """Test finding recent messages."""
    # Create multiple messages
    messages = []
    for i in range(5):
        # Add a small delay to ensure different timestamps
        import time
        time.sleep(0.01)

        message = Message.create(
            db,
            user_id=test_user["_id"],
            artwork_id=test_artwork["_id"]
        )
        messages.append(message)

    # Get recent messages
    recent_messages = Message.find_recent(db, limit=3)

    # Should have exactly 3 messages (due to limit)
    assert len(recent_messages) == 3

    # Messages should be in reverse chronological order (newest first)
    for i in range(len(recent_messages) - 1):
        assert recent_messages[i]["timestamp"] >= recent_messages[i+1]["timestamp"]

    # The most recent messages should be the ones we created last
    assert recent_messages[0]["_id"] == messages[-1]["_id"]


def test_mark_seen(db, test_message, test_user):
    """Test marking a message as seen by another user."""
    # Create another user who will mark the message as seen
    from app.models.user import User
    another_user = User.create(
        db,
        username="anotheruser",
        email="another@example.com",
        password="password123",
        display_name="Another User"
    )

    # Initially, only the sender has seen the message
    original_message = Message.find_one(db, test_message["_id"])
    assert len(original_message["seen_by"]) == 1
    assert ObjectId(test_user["_id"]) in original_message["seen_by"]

    # Mark as seen by another user
    Message.mark_seen(db, test_message["_id"], another_user["_id"])

    # Check that the message is now seen by both users
    updated_message = Message.find_one(db, test_message["_id"])
    assert len(updated_message["seen_by"]) == 2
    assert ObjectId(test_user["_id"]) in updated_message["seen_by"]
    assert ObjectId(another_user["_id"]) in updated_message["seen_by"]

    # Marking as seen again by the same user shouldn't add duplicate entries
    Message.mark_seen(db, test_message["_id"], another_user["_id"])
    rechecked_message = Message.find_one(db, test_message["_id"])
    assert len(rechecked_message["seen_by"]) == 2


def test_get_with_details(db, test_message, test_user, test_artwork):
    """Test getting a message with user and artwork details."""
    # Get message with details
    message_with_details = Message.get_with_details(db, test_message["_id"])

    # Check that we got the message with the joined details
    assert message_with_details is not None
    assert "user" in message_with_details
    assert "artwork" in message_with_details

    # Check user details
    assert message_with_details["user"]["_id"] == test_user["_id"]
    assert message_with_details["user"]["username"] == test_user["username"]
    assert message_with_details["user"]["display_name"] == test_user["display_name"]

    # Check artwork details
    assert message_with_details["artwork"]["_id"] == test_artwork["_id"]
    assert message_with_details["artwork"]["title"] == test_artwork["title"]
    assert message_with_details["artwork"]["file_path"] == test_artwork["file_path"]
