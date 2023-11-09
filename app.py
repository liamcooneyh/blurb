from flask import Flask, session
from auth import auth_bp
from landing_page import landing_bp
from user_profile import user_profile_bp
from current_track import current_track_bp
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = '7d266374106b85802220b6d77d03214f05f6581d45ee9d7c25c4984b2d0f972e'

# Retrieve environment variables 
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

app.register_blueprint(auth_bp)
app.register_blueprint(landing_bp)
app.register_blueprint(user_profile_bp)
app.register_blueprint(current_track_bp)

