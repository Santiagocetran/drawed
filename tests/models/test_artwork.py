import pytest
from bson import ObjectId
from datetime import datetime

from app.models.artwork import Artwork


def test_artwork_creation(db):
    """Test creating a new artwork."""
    artwork = Artwork.create(
        db,
        title="Mona Lisa",
        file_path="/artworks/mona_lisa.jpg"
    )

    # Check that artwork was created with all fields
    assert artwork is not None
    assert isinstance(artwork["_id"], ObjectId)
    assert artwork["title"] == "Mona Lisa"
    assert artwork["file_path"] == "/artworks/mona_lisa.jpg"
    assert "created_at" in artwork
    assert isinstance(artwork["created_at"], datetime)


def test_find_artwork(db, test_artwork):
    """Test finding an artwork by ID."""
    artwork = Artwork.find_one(db, test_artwork["_id"])

    assert artwork is not None
    assert artwork["title"] == test_artwork["title"]
    assert artwork["file_path"] == test_artwork["file_path"]


def test_find_all_artworks(db, test_artwork):
    """Test finding all artworks."""
    # Create a second artwork to test finding multiple
    second_artwork = Artwork.create(
        db,
        title="Starry Night",
        file_path="/artworks/starry_night.jpg"
    )

    # Get all artworks
    artworks = Artwork.find_all(db)

    # Should have at least 2 artworks (the test fixture + our new one)
    assert len(artworks) >= 2

    # Find our specific artworks in the results
    artwork_ids = [artwork["_id"] for artwork in artworks]
    assert test_artwork["_id"] in artwork_ids
    assert second_artwork["_id"] in artwork_ids


def test_find_all_with_limit(db):
    """Test finding artworks with a limit."""
    # Create multiple artworks
    for i in range(5):
        Artwork.create(
            db,
            title=f"Test Artwork {i}",
            file_path=f"/artworks/test_{i}.jpg"
        )

    # Get artworks with a limit
    limited_artworks = Artwork.find_all(db, limit=3)

    # Should have exactly 3 artworks
    assert len(limited_artworks) == 3


def test_random_artwork(db):
    """Test getting a random artwork."""
    # Create multiple artworks to ensure we have some to choose from
    artworks = []
    for i in range(5):
        artwork = Artwork.create(
            db,
            title=f"Random Test Artwork {i}",
            file_path=f"/artworks/random_test_{i}.jpg"
        )
        artworks.append(artwork)

    # Get a random artwork
    random_artwork = Artwork.random(db)

    # Check that we got an artwork
    assert random_artwork is not None
    assert "title" in random_artwork
    assert "file_path" in random_artwork

    # Since it's random, we can't check for a specific one,
    # but we can check that it has the expected structure
    assert isinstance(random_artwork["_id"], ObjectId)
    assert isinstance(random_artwork["created_at"], datetime)
