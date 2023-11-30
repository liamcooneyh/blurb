# Combined script (app.py)
import sys 
print(f"Sys Path:")

sys.exit() 

from flask import Flask, Blueprint, jsonify, render_template, request, redirect, url_for, session
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import spotipy
import requests
import os
from dotenv import load_dotenv

load_dotenv()

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
        print("Redirecting to auth_url:", auth_url)  # Debug statement
        return redirect(auth_url)

    return redirect('/landing')  # Send authenticated user to the landing page


@auth_bp.route('/callback')
def callback():
    auth_code = request.args.get('code')
    error = request.args.get('error')

    if error:
        # Handle the error scenario (e.g., user denied the permission)
        print("Error received from Spotify:", error)  # Debug statement
        return f"Error received from Spotify: {error}", 400

    if not auth_code:
        print("Authorization code not found in the URL")  # Debug statement
        return 'Authorization code not found in the URL', 400

    try:
        token_info = sp_oauth.get_access_token(auth_code)
    except Exception as e:
        # Log the exception for debugging
        print(f"Error obtaining access token: {e}")
        return 'Failed to obtain access token', 500

    if not token_info:
        print("Failed to obtain access token")  # Debug statement
        return 'Failed to obtain access token', 500

    # Store the token information in the session or a database for later use
    session['token_info'] = token_info

    # Redirect to React app
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

        print("User information retrieved:", user_info)  # Debug statement
        return render_template('landing.html', user_info=user_info)
    else:
        print("Token is expired or missing, redirecting to auth_url")  # Debug statement
        # Token is expired or missing, redirect to the authorization page
        auth_url = sp_oauth.get_authorize_url()
        print("Redirecting to auth_url:", auth_url)  # Debug statement
        return redirect(auth_url)

app.register_blueprint(landing_bp)


##########################
##### GENERIC ROUTES #####
##########################
@app.route('/api/get-token')
# Can use this method for sending user data to React (e.g 'api/get-current-song)
def get_token():
    token_info = session.get('token_info')

    if token_info:
        return jsonify({'access_token': token_info['access_token']}), 200
    
    else:
        return jsonify({'error': 'Token not found'}), 404


@app.route('/error')
def error():
    return "An error occurred."


# Run the Flask app
if __name__ == '__main__':
    app.run()
