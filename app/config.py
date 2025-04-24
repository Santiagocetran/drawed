import os
from datetime import timedelta

class Config:
    # Flask core settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    DEBUG = False
    TESTING = False
    
    # MongoDB settings
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/drawed'
    
    # Flask-SocketIO settings
    SOCKETIO_ASYNC_MODE = 'eventlet'  # 'eventlet', 'gevent', or None for threading (less performant)
    
    # Application specific settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'artworks')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size

class DevelopmentConfig(Config):
    DEBUG = True
    # You might want specific MongoDB for development
    MONGO_URI = os.environ.get('DEV_MONGO_URI') or 'mongodb://localhost:27017/drawed_dev'

class TestingConfig(Config):
    TESTING = True
    # Use a separate test database
    MONGO_URI = os.environ.get('TEST_MONGO_URI') or 'mongodb://localhost:27017/drawed_test'

class ProductionConfig(Config):
    # In production, all secrets should come from environment variables
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MONGO_URI = os.environ.get('MONGO_URI')
    
    # Production might use a different SocketIO mode for better performance
    SOCKETIO_ASYNC_MODE = 'eventlet'

# Create a config dictionary to easily select configs based on environment
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}