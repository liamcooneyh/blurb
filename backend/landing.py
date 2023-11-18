# landing.py
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

landing_bp = Blueprint('landing', __name__)
sp_oauth = SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope='user-top-read')


# Displays the information on the landing page, some information about the user
@landing_bp.route('/landing')
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
        top_artists = sp.current_user_top_artists()
        top_artist = top_artists['items'][0]['name']

        # Uncomment this line to print user_info for debugging
        # print(user_info)
        # print(top_artists['items'][0]['name']) # gets top artist for the user

        return render_template('landing.html', user_info=user_info, top_artist=top_artist)
    else:
        # Token is expired or missing, redirect to the authorization page
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)







