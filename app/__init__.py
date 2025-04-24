# Simply mark the directory as a package
# You can also expose specific components here if needed
from app.core import create_app, socketio

# This allows imports like: from app import create_app, socketio