# landing_page.py
from flask import Blueprint, render_template

import os
from dotenv import load_dotenv
load_dotenv()

# Retrieve environment variables 
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

landing_bp = Blueprint('landing', __name__)

@landing_bp.route('/landing')
def landing():
    return render_template('landing_page.html')
