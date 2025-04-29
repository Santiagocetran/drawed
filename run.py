from app import create_app, socketio
import os

# Get environment from ENV variable or default to development
config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    # Use socketio.run instead of app.run for WebSocket support
    socketio.run(app, host='0.0.0.0', debug=app.config['DEBUG'])