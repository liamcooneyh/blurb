# app.py

########################
### IMPORT LIBRARIES ###
########################
import logging
from flask import Flask, Blueprint, jsonify, render_template, request, redirect, url_for, session
from flask_cors import CORS
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import spotipy
import requests
import os
from dotenv import load_dotenv
from v1_api import init_api_blueprint

# Load environment variables
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

# Enable CORS for development
CORS(app)
# CORS(app, resources={r"/v1/api/*": {"origins": "http://localhost:3000"}})

# Spotify OAuth setup
sp_oauth = SpotifyOAuth(CLIENT_ID, 
                        CLIENT_SECRET,
                        REDIRECT_URI, 
                        scope='user-top-read')


################################
####### IMPORT BLUEPRINTS ######
################################
# Initialize API Blueprint with Spotify client and OAuth object
v1_api_bp = init_api_blueprint(spotify, sp_oauth)

# Register the API Blueprint
app.register_blueprint(v1_api_bp)


################################
### AUTHENTICATION BLUEPRINT ###
################################
auth_bp = Blueprint('auth', __name__)

# Define routes for auth_bp (from auth.py)
@auth_bp.route('/')
def index(): 
    if not session.get('token_info'):       
        auth_url = sp_oauth.get_authorize_url()  # Generates URL for Spotify OAuth login page
        logging.info("Redirecting to auth_url: %s", auth_url) 
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


##########################
####### API ROUTES #######
##########################
# Get authentication token



##########################
##### GENERIC ROUTES #####
##########################
@app.route('/error')
def error():
    return "An error occurred."


# Run the Flask app
if __name__ == '__main__':
    app.run()
