# Combined script (app.py)
import logging
from flask import Flask, Blueprint, jsonify, render_template, request, redirect, url_for, session
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import spotipy
import requests
import os
from dotenv import load_dotenv
import pprint
from functools import wraps
from datetime import datetime

load_dotenv()

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s] - %(message)s')

# Retrieve environment variables
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')

# Create SpotifyClientCredentials instance with credentials
client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

# Initialize a Spotify client
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Initialize Flask app
app = Flask(__name__)
app.debug = True
app.secret_key = FLASK_SECRET_KEY

# Spotify OAuth setup
sp_oauth = SpotifyOAuth(CLIENT_ID, 
                        CLIENT_SECRET,
                        REDIRECT_URI, 
                        scope='user-top-read')

################################
### AUTHENTICATION BLUEPRINT ###
################################
auth_bp = Blueprint('auth', __name__)

# Define routes for auth_bp (from auth.py)
@auth_bp.route('/')
def index(): 
    if not session.get('token_info'):       
        auth_url = sp_oauth.get_authorize_url()  # Generates URL for Spotify OAuth login page
        logging.info("Redirecting to auth_url: %s", auth_url)  # Log statement
        return redirect(auth_url)

    # Send authenticated user to the React landing page
    logging.info("User already authenticated, redirecting to React landing page")
    return redirect('http://localhost:3000/') 


@auth_bp.route('/callback')
def callback():
    auth_code = request.args.get('code')
    error = request.args.get('error')

    if error:
        # Handle the error scenario (e.g., user denied the permission)
        logging.error("Error received from Spotify: %s", error)
        return f"Error received from Spotify: {error}", 400

    if not auth_code:
        logging.error("Authorization code not found in the URL")
        return 'Authorization code not found in the URL', 400

    try:
        token_info = sp_oauth.get_access_token(auth_code)
    except Exception as e:
        # Log the exception for debugging
        logging.error("Error obtaining access token: %s", e)
        return 'Failed to obtain access token', 500

    if not token_info:
        logging.error("Failed to obtain access token")
        return 'Failed to obtain access token', 500

    # Store the token information in the session or a database for later use
    session['token_info'] = token_info

    # Redirect to React app
    logging.info("Redirecting to React landing page after successful authentication")
    return redirect('http://localhost:3000/landing')

# Register the authentication blueprint
app.register_blueprint(auth_bp)


# Spotify auth decorator
def spotify_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token_info = session.get('token_info')

        if not token_info:
            logging.error("Token not found in the session")
            return jsonify({'error': 'Token not found'}), 404

        try:
            if is_token_expired(token_info):
                token_info = refresh_token(token_info)
                session['token_info'] = token_info  # Update the session with the refreshed token

            return f(spotify=spotipy.Spotify(auth=token_info['access_token']), *args, **kwargs)
        except Exception as e:
            logging.error("Error: %s", e)
            return jsonify({'error': str(e)}), 500

    return decorated_function

# Logic for expired token
def is_token_expired(token_info):
    # Check if the current time is greater than the expiry time
    now = datetime.now().timestamp()
    return token_info['expires_at'] - now < 60  # Refresh if less than 60 seconds remaining

# Logic to refresh token
def refresh_token(token_info):
    # Refresh the token using the SpotifyOAuth instance
    refreshed_token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return refreshed_token_info



##########################
####### API ROUTES #######
##########################
@app.route('/api/user-info')
@spotify_auth_required
def get_user_data(spotify):
    user_info = spotify.me()
    logging.info("User information retrieved from Spotify API: %s", user_info)
    return jsonify({'user_info': user_info}), 200

@app.route('/api/testing')
@spotify_auth_required
def get_recent_tracks(spotify):
    recent_tracks = spotify.current_user_saved_albums()
    return jsonify(recent_tracks), 200


@app.route('/error')
def error():
    return "An error occurred."


# Run the Flask app
if __name__ == '__main__':
    app.run()
