from flask import Blueprint, render_template, send_from_directory, current_app
import os

# Create a blueprint
views_bp = Blueprint('views', __name__)


@views_bp.route('/')
def index():
    """Landing page route"""
    return render_template('index.html', title='Drawed - Share Art')


@views_bp.route('/artworks/<path:filename>')
def serve_artwork(filename):
    """Serve artwork files"""
    try:
        # First try to serve from static/artworks
        static_artworks = os.path.join(current_app.static_folder, 'artworks')
        return send_from_directory(static_artworks, filename)
    except:
        # Fall back to the artworks directory in project root
        artworks_dir = os.path.join(current_app.config['UPLOAD_FOLDER'])
        return send_from_directory(artworks_dir, filename)
