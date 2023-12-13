# Combined script (app.py)
import logging
from flask import Flask, Blueprint, jsonify, render_template, request, redirect, url_for, session
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import spotipy
import requests
import os
from dotenv import load_dotenv
import pprint

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


#########################
### LANDING BLUEPRINT ###
#########################
# Define other routes or blueprints (from app.py)
landing_bp = Blueprint('landing', __name__)

# Displays the information on the landing page, some information about the user
@landing_bp.route('/landing')
def landing():
    token_info = sp_oauth.get_cached_token()  # Get access token from cookies

    if token_info and not sp_oauth.is_token_expired(token_info):
        # Stores the session token info for later use
        session['token_info'] = token_info

        # Create Spotipy client with the access token
        sp = spotipy.Spotify(auth=token_info['access_token'])

        # Make a request and get the user's information
        user_info = sp.me()

        logging.info("User information retrieved: %s", user_info)  # Log statement
        return render_template('landing.html', user_info=user_info)
    else:
        logging.warning("Token is expired or missing, redirecting to auth_url")
        # Token is expired or missing, redirect to the authorization page
        auth_url = sp_oauth.get_authorize_url()
        logging.info("Redirecting to auth_url: %s", auth_url)  # Log statement
        return redirect(auth_url)

app.register_blueprint(landing_bp)


##########################
####### API ROUTES #######
##########################
@app.route('/api/get-token')
# Can use this method for sending user data to React (e.g 'api/get-current-song)
def get_token():
    token_info = session.get('token_info')

    if token_info:
        return jsonify({'access_token': token_info['access_token']}), 200
    
    else:
        logging.error("Token not found in the session")
        return jsonify({'error': 'Token not found'}), 404
    

@app.route('/api/user-info')
def get_user_data():
    token_info = session.get('token_info')

    if token_info:
        try:
            user_info = spotify.me()
            logging.info("User information retrieved from Spotify API: %s", user_info)  # Log statement
            return jsonify({'user_info': user_info}), 200
        except Exception as e:
            logging.error("Error fetching user information from Spotify API: %s", e)  # Log statement
            return jsonify({'error': str(e)}), 500
    else:
        logging.error("Token not found in the session")
        return jsonify({'error': 'Token not found'}), 404


@app.route('/error')
def error():
    return "An error occurred."


# Run the Flask app
if __name__ == '__main__':
    app.run()
