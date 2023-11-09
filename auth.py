# auth.py
from flask import Blueprint, redirect, render_template, session
from spotipy.oauth2 import SpotifyOAuth

auth_bp = Blueprint('auth', __name__)
sp_oauth = SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope='user-library-read')

@auth_bp.route('/')
def index():
    if not session.get('token_info'):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    return redirect('/landing')
