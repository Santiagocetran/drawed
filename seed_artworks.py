#!/usr/bin/env python3
"""
Seed script to populate the database with initial artwork data.
This script should be run once to create a base set of artwork in the database.
"""

import os
import sys
from app import create_app
from app.database import get_db
from app.models.artwork import Artwork

# Sample artwork data
SAMPLE_ARTWORKS = [
    {
        "title": "Starry Night",
        "file_path": "/static/artworks/starry_night.jpg"
    },
    {
        "title": "The Scream",
        "file_path": "/static/artworks/the_scream.jpg"
    },
    {
        "title": "Mona Lisa",
        "file_path": "/static/artworks/mona_lisa.jpg"
    },
    {
        "title": "The Persistence of Memory",
        "file_path": "/static/artworks/persistence_of_memory.jpg"
    },
    {
        "title": "The Birth of Venus",
        "file_path": "/static/artworks/birth_of_venus.jpg"
    },
    {
        "title": "Girl with a Pearl Earring",
        "file_path": "/static/artworks/girl_with_pearl_earring.jpg"
    },
    {
        "title": "The Great Wave off Kanagawa",
        "file_path": "/static/artworks/great_wave.jpg"
    },
    {
        "title": "The Night Watch",
        "file_path": "/static/artworks/night_watch.jpg"
    },
    {
        "title": "Water Lilies",
        "file_path": "/static/artworks/water_lilies.jpg"
    },

]


def create_artwork_directory(app):
    """Create the artwork directory if it doesn't exist"""
    static_art_dir = os.path.join(app.static_folder, 'artworks')
    if not os.path.exists(static_art_dir):
        print(f"Creating artwork directory: {static_art_dir}")
        os.makedirs(static_art_dir)
    return static_art_dir


def seed_artworks():
    """Seed the database with sample artwork"""
    # Create Flask app context
    app = create_app('development')

    with app.app_context():
        db = get_db()

        # Create the artwork directory
        artwork_dir = create_artwork_directory(app)

        # Check if artworks already exist
        existing_count = len(list(Artwork.get_collection(db).find()))
        if existing_count > 0:
            print(
                f"There are already {existing_count} artworks in the database.")
            response = input(
                "Do you want to add more artwork samples? (y/n): ")
            if response.lower() != 'y':
                print("Operation cancelled.")
                return

        # First, clear out any existing data if needed
        clear_data = input(
            "Do you want to clear existing artwork data? (y/n): ")
        if clear_data.lower() == 'y':
            Artwork.get_collection(db).delete_many({})
            print("Cleared existing artwork data")

        # Insert sample artworks
        for artwork_data in SAMPLE_ARTWORKS:
            # Check if this artwork already exists
            existing = Artwork.get_collection(db).find_one(
                {"title": artwork_data["title"]})
            if existing:
                print(
                    f"Artwork '{artwork_data['title']}' already exists, skipping.")
                continue

            # Create the artwork
            artwork = Artwork.create(
                db,
                title=artwork_data["title"],
                file_path=artwork_data["file_path"]
            )

            print(
                f"Created artwork: {artwork['title']} (ID: {artwork['_id']})")

            file_path = artwork_data["file_path"].replace("/static/", "")
            full_path = os.path.join(app.static_folder, file_path)

            if not os.path.exists(os.path.dirname(full_path)):
                os.makedirs(os.path.dirname(full_path))

            if not os.path.exists(full_path):
                print(f"Creating placeholder image: {full_path}")

                try:
                    # Try to download sample artwork from placeholder service
                    import requests
                    # Use a more reliable placeholder service
                    placeholder_url = f"https://picsum.photos/800/600"
                    response = requests.get(placeholder_url, stream=True)
                    response.raise_for_status()

                    with open(full_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)

                    print(
                        f"✓ Downloaded image for {artwork_data['title']} to {full_path}")

                except Exception as e:
                    print(f"Failed to download image: {e}")
                    print("Trying alternative placeholder source...")
                    try:
                        placeholder_url = f"https://via.placeholder.com/800x600?text={artwork_data['title'].replace(' ', '+')}"
                        response = requests.get(placeholder_url, stream=True)
                        response.raise_for_status()

                        with open(full_path, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                f.write(chunk)

                        print(
                            f"✓ Downloaded placeholder image for {artwork_data['title']}")
                    except Exception as e2:
                        print(f"Failed to download placeholder: {e2}")
                        print("Creating empty file instead")
                        with open(full_path, 'w') as f:
                            f.write(
                                "This is a placeholder for artwork. Replace with actual image file.")

        print("Artwork seeding completed.")


if __name__ == "__main__":
    seed_artworks()
