from flask import request, session, current_app
from flask_socketio import emit, join_room, leave_room
from app import socketio
from app.database import get_db
from app.models.artwork import Artwork
from app.models.message import Message
from app.models.user import User
from datetime import datetime
from bson import ObjectId


@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    # For now, use a default guest user ID if none exists
    # In a real app, you would use authentication here
    if 'user_id' not in session:
        # Create a guest user in the database to get a proper ObjectId
        db = get_db()
        guest_name = f"guest_{datetime.utcnow().timestamp()}"
        try:
            user = User.create(
                db,
                username=guest_name,
                email=f"{guest_name}@example.com",
                password="guest_password",  # This is just a placeholder
                display_name="Guest User"
            )
            # Store the ObjectId as a string in the session
            session['user_id'] = str(user['_id'])
            session.modified = True
        except ValueError:
            # If username is taken, try again with a different timestamp
            guest_name = f"guest_{datetime.utcnow().timestamp()}"
            user = User.create(
                db,
                username=guest_name,
                email=f"{guest_name}@example.com",
                password="guest_password",
                display_name="Guest User"
            )
            session['user_id'] = str(user['_id'])
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

    # Get user_id from session (should be a string)
    user_id = session.get('user_id')
    if not user_id:
        # Handle case where user isn't in session
        emit('error', {
            'message': "Session error. Please refresh the page.",
            'timestamp': datetime.utcnow().isoformat()
        })
        return

    # Get a random artwork from the database
    artwork = Artwork.random(db)

    # If no artwork is found, return an error message
    if not artwork:
        emit('error', {
            'message': "No artwork found in the database",
            'timestamp': datetime.utcnow().isoformat()
        })
        return

    # Create the message
    try:
        message = Message.create(
            db,
            user_id=user_id,
            artwork_id=str(artwork['_id'])
        )

        # Find user info for the message
        user = User.find_one(db, ObjectId(user_id))

        # Broadcast the message to all clients in the room
        emit('new_art', {
            'message_id': str(message['_id']),
            'user_id': user_id,
            'username': user['username'],
            'display_name': user['display_name'],
            'artwork': {
                'id': str(artwork['_id']),
                'title': artwork['title'],
                'file_path': artwork['file_path']
            },
            'timestamp': message['timestamp'].isoformat()
        }, room='main_room')
    except Exception as e:
        # Log the error and send error message
        print(f"Error sending art: {str(e)}")
        emit('error', {
            'message': f"Error sending artwork: {str(e)}",
            'timestamp': datetime.utcnow().isoformat()
        })


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

    try:
        # Mark the message as seen
        Message.mark_seen(db, data['message_id'], user_id)
    except Exception as e:
        print(f"Error marking message as seen: {str(e)}")
