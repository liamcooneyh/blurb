# # auth.py
# from flask import Flask, Blueprint, render_template, request, redirect, url_for, session
# from spotipy.oauth2 import SpotifyOAuth
# import spotipy
# import requests
# import os
# from dotenv import load_dotenv

# load_dotenv()

# CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
# CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
# REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

# auth_bp = Blueprint('auth', __name__)
# sp_oauth = SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope='user-top-read')

# # Authenticates the user and brings them to the landing page if successful
# @auth_bp.route('/')
# def index(): 
#     if not session.get('token_info'):
#         auth_url = sp_oauth.get_authorize_url() 
#         return redirect(auth_url)

#     # Handle authenticated user's actions here
#     return redirect('/landing')


# @auth_bp.route('/callback')
# def callback():
#     auth_code = request.args.get('code')
#     error = request.args.get('error')

#     if error:
#         # Handle the error scenario (e.g., user denied the permission)
#         return f"Error received from Spotify: {error}", 400

#     if not auth_code:
#         return 'Authorization code not found in the URL', 400

#     try:
#         token_info = sp_oauth.get_access_token(auth_code)

#     except Exception as e:
#         # Log the exception for debugging
#         print(f"Error obtaining access token: {e}")
#         return 'Failed to obtain access token', 500

#     if not token_info:
#         return 'Failed to obtain access token', 500

#     # Store the token information in the session or a database for later use
#     session['token_info'] = token_info

#     return redirect('/landing')

