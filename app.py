# app.py
from flask import Flask
from auth import auth_bp
from landing import landing_bp

# Import other blueprints as needed
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.debug = True
app.secret_key = os.getenv('FLASK_SECRET_KEY')  

# Retrieve environment variables
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

app.register_blueprint(auth_bp)
app.register_blueprint(landing_bp)
# Register other blueprints as needed
