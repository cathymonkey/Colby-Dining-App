from flask import Flask
from models import db, Food, Tag, food_tags
from flask_login import LoginManager
from views import main_blueprint
from datetime import time
from utils import create_tags
from models import db
from views import main_blueprint
from auth import auth_bp, google_bp, login_manager, init_admin_model
import os
from dotenv import load_dotenv

# Set environment variable for development
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' 


app = Flask(__name__, static_folder='static')

# Configuration
app.config['SECRET_KEY'] = 'secret keyyyyy'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# OAuth config
app.config['GOOGLE_OAUTH_CLIENT_ID'] = "1015740593977-rgj3g9af6jschsnd9jjh0ham19b1bi62.apps.googleusercontent.com"
app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = "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"

# Fix for OAuth HTTPS requirement in development
app.config['OAUTHLIB_RELAX_TOKEN_SCOPE'] = True
app.config['OAUTHLIB_INSECURE_TRANSPORT'] = True

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)

# Initialize admin model
init_admin_model()

# Register blueprints 
app.register_blueprint(auth_bp) 
app.register_blueprint(google_bp, url_prefix="/login") 
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables (if not created)
        create_tags()
        db.create_all()

    app.run(debug=True, port=8000)