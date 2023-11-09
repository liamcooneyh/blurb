# current_track.py
from flask import Blueprint, render_template, session
from spotipy import Spotify

import os
from dotenv import load_dotenv
load_dotenv()

# Retrieve environment variables 
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

current_track_bp = Blueprint('current_track', __name__)

@current_track_bp.route('/current_track')
def current_track():
    token_info = session.get('token_info')
    if token_info:
        sp = Spotify(auth=token_info['access_token'])
        # Check and refresh token as needed...
        current_track = sp.current_playback()
        # Render the current_track template...
    else:
        return 'Error: User not authenticated.'
