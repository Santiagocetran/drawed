from flask import request, session, current_app
from flask_socketio import emit, join_room, leave_room
from app import socketio
from app.database import get_db
from app.models.artwork import Artwork
from app.models.message import Message
from app.models.user import User
from datetime import datetime


@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    # For now, use a default guest user ID if none exists
    # In a real app, you would use authentication here
    if 'user_id' not in session:
        session['user_id'] = 'guest_' + str(datetime.utcnow().timestamp())
        session.modified = True

    # Join the main room
    join_room('main_room')

    # Emit a welcome message
    emit('status', {
        'message': f"Connected to chat server",
        'count': 0,  # You might want to get the actual count from the database
        'timestamp': datetime.utcnow().isoformat()
    })


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    leave_room('main_room')


@socketio.on('send_art')
def handle_send_art(data):
    """Handle a request to send random artwork"""
    db = get_db()

    # Use a guest ID for now (would use authenticated user_id in production)
    user_id = session.get('user_id', 'guest_' +
                          str(datetime.utcnow().timestamp()))

    # Get a random artwork from the database
    artwork = Artwork.random(db)

    # If no artwork is found, return an error message
    if not artwork:
        emit('error', {
            'message': "No artwork found in the database",
            'timestamp': datetime.utcnow().isoformat()
        })
        return

    # Create a new message in the database
    # In a real app, you would use an actual user ID from authentication
    # For now, we'll create a dummy user record if needed
    if user_id.startswith('guest_'):
        # Check if we already have a user record for this guest
        user = User.find_by_username(db, user_id)
        if not user:
            try:
                user = User.create(
                    db,
                    username=user_id,
                    email=f"{user_id}@example.com",
                    password="guest_password",  # This is just a placeholder
                    display_name=f"Guest User"
                )
            except ValueError:
                # If username is taken, generate a new one
                user_id = 'guest_' + str(datetime.utcnow().timestamp())
                user = User.create(
                    db,
                    username=user_id,
                    email=f"{user_id}@example.com",
                    password="guest_password",
                    display_name=f"Guest User"
                )
        user_id = str(user['_id'])

    # Create the message
    message = Message.create(
        db,
        user_id=user_id,
        artwork_id=str(artwork['_id'])
    )

    # Broadcast the message to all clients in the room
    emit('new_art', {
        'message_id': str(message['_id']),
        'user_id': user_id,
        'username': User.find_one(db, user_id)['username'],
        'display_name': User.find_one(db, user_id)['display_name'],
        'artwork': {
            'id': str(artwork['_id']),
            'title': artwork['title'],
            'file_path': artwork['file_path']
        },
        'timestamp': message['timestamp'].isoformat()
    }, room='main_room')


@socketio.on('mark_seen')
def handle_mark_seen(data):
    """Mark a message as seen by the current user"""
    if 'message_id' not in data:
        return

    db = get_db()
    user_id = session.get('user_id')

    # Only proceed if we have a user ID
    if not user_id:
        return

    # Mark the message as seen
    Message.mark_seen(db, data['message_id'], user_id)
