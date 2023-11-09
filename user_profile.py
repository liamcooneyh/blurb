# user_profile.py
from flask import Blueprint, render_template, session
from spotipy import Spotify

import os
from dotenv import load_dotenv
load_dotenv()

# Retrieve environment variables 
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

user_profile_bp = Blueprint('user_profile', __name__)

@user_profile_bp.route('/user_profile')
def user_profile():
    token_info = session.get('token_info')
    if token_info:
        sp = Spotify(auth=token_info['access_token'])
        user_data = sp.current_user()
        return render_template('user_profile.html', user_data=user_data)
    else:
        return 'Error: User not authenticated. <a href="/">Authenticate with Spotify</a>'
