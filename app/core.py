from flask import Flask
from flask_socketio import SocketIO
from .config import Config

socketio = SocketIO()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Register blueprints
    from app.routes.views import views_bp
    app.register_blueprint(views_bp)
    
    # Import socket events
    from app.sockets import events
    
    return app