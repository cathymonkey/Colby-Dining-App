from flask import Flask
from models import db, Food, Tag, food_tags
from flask_login import LoginManager
from views import main_blueprint
from datetime import time
from utils import create_tags
from auth import auth_bp, google_bp, login_manager, init_admin_model
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='static')

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# OAuth config
app.config['GOOGLE_OAUTH_CLIENT_ID'] = os.getenv('GOOGLE_OAUTH_CLIENT_ID')
app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET')
app.config['OAUTHLIB_RELAX_TOKEN_SCOPE'] = True
app.config['OAUTHLIB_INSECURE_TRANSPORT'] = os.getenv('FLASK_ENV') == 'development'

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
    app.run(debug=False)


with app.app_context():
    try:
        db.create_all()
        create_tags()
    except Exception as e:
        print(f"Database initialization error: {e}")