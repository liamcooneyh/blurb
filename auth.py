# auth.py
from flask import Blueprint, redirect, render_template, session
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

auth_bp = Blueprint('auth', __name__)
sp_oauth = SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope='user-library-read')

@auth_bp.route('/')
def index():
    if not session.get('token_info'):
        auth_url = sp_oauth.get_authorize_url()
        print('test')
        return redirect(auth_url)

    # Handle authenticated user's actions here
    return redirect('/landing')

@auth_bp.route('/landing')
def landing():
    return render_template('landing.html')