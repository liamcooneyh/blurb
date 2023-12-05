# v1_api.py
from flask import Blueprint, jsonify, session
import logging

# Initialize Blueprint
v1_api_bp = Blueprint('v1_api', __name__, url_prefix='/v1/api')

# Function to initialize the API Blueprint
def init_api_blueprint(spotify, sp_oauth):
    global _spotify, _sp_oauth
    _spotify = spotify
    _sp_oauth = sp_oauth
    return v1_api_bp

###############################
######### AUTH ROUTES #########
###############################
@v1_api_bp.route('/v1/api/get-token')
def get_token():
    token_info = _sp_oauth.get_cached_token()  # Get access token from cookies

    if token_info and not _sp_oauth.is_token_expired(token_info):
        # Stores the session token info for later use
        session['token_info'] = token_info

        return jsonify({'access_token': token_info['access_token']}), 200
    
    else:
        logging.warning("Token is expired or missing, redirecting to auth_url")
        # Token is expired or missing, redirect to the authorization page
       
        auth_url = _sp_oauth.get_authorize_url()
        
        logging.info("Redirecting to auth_url: %s", auth_url)  # Log statement
        logging.error("Token not found in the session")
        
        return jsonify({'error': 'Token not found'}), 404










