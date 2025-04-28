from flask import current_app, g
from pymongo import MongoClient


def get_db():
    """
    Configure and return the MongoDB client.
    Uses the application's MONGO_URI config value.
    """
    if 'db' not in g:
        client = MongoClient(current_app.config['MONGO_URI'])
        g.db = client.get_default_database()
    return g.db


def close_db(e=None):
    """
    Close the MongoDB connection.
    """
    db = g.pop('db', None)
    if db is not None:
        db.client.close()


def init_app(app):
    """
    Register database functions with the Flask app.
    """
    app.teardown_appcontext(close_db)
