from flask import Blueprint, render_template

# Create a blueprint
views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def index():
    """Landing page route"""
    return render_template('index.html', title='Drawed - Hello World')