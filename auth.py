# auth.py
from flask import Flask, Blueprint, render_template, request, redirect, url_for, session
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import requests
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

auth_bp = Blueprint('auth', __name__)
sp_oauth = SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope='user-library-read')

# Authenticates the user and brings them to the landing page if successful
@auth_bp.route('/')
def index(): 
    if not session.get('token_info'):
        auth_url = sp_oauth.get_authorize_url() 
        return redirect(auth_url)

    # Handle authenticated user's actions here
    return redirect('/landing')


@auth_bp.route('/callback')
def callback():
    auth_code = request.args.get('code')
    error = request.args.get('error')

    if error:
        # Handle the error scenario (e.g., user denied the permission)
        return f"Error received from Spotify: {error}", 400

    if not auth_code:
        return 'Authorization code not found in the URL', 400

    try:
        token_info = sp_oauth.get_access_token(auth_code)
    except Exception as e:
        # Log the exception for debugging
        print(f"Error obtaining access token: {e}")
        return 'Failed to obtain access token', 500

    if not token_info:
        return 'Failed to obtain access token', 500

    # Store the token information in the session or a database for later use
    session['token_info'] = token_info

    return redirect('/landing')


# Displays the information on the landing page, some information about the user
@auth_bp.route('/landing')
def landing():
    # Get access token from cookies
    token_info = sp_oauth.get_cached_token()

    if token_info and not sp_oauth.is_token_expired(token_info):
        # Stores the session token info for later use
        session['token_info'] = token_info

        # Create Spotipy client with the access token
        sp = spotipy.Spotify(auth=token_info['access_token'])

        # Make a request and get the user's information
        user_info = sp.me()

        # Uncomment this line to print user_info for debugging
        # print(user_info)

        return render_template('landing.html', user_info=user_info)
    else:
        # Token is expired or missing, redirect to the authorization page
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)


