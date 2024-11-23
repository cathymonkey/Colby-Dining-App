import logging
import os
import sys

from dotenv import load_dotenv
from flask import Flask

from auth import auth_bp, google_bp, login_manager, init_admin_model
from feedback import feedback_bp
from gemini import gemini_bp  # Import the blueprint
from models import db
from news import news_bp
from utils import create_tags
from views import main_blueprint

# Set up logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='static')

logger.info("Starting application initialization...")

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
database_url = os.getenv('JAWSDB_URL')
if database_url:
    database_url = database_url.replace('mysql://', 'mysql+mysqlconnector://')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    logger.info("Using JawsDB URL for database connection")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    logger.info("Using default database URL")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

logger.info("Database URL configured")

# OAuth config
app.config['GOOGLE_OAUTH_CLIENT_ID'] = os.getenv('GOOGLE_OAUTH_CLIENT_ID')
app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET')
app.config['OAUTHLIB_RELAX_TOKEN_SCOPE'] = True
app.config['OAUTHLIB_INSECURE_TRANSPORT'] = os.getenv('FLASK_ENV') == 'development'


# Initialize extensions
try:
    db.init_app(app)
    logger.info("Database initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize database: {e}")
    raise
try:
    login_manager.init_app(app)
    logger.info("Login manager initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize login manager: {e}")
    raise

# Initialize admin model
try:
    init_admin_model()
    logger.info("Admin model initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize admin model: {e}")
    raise

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(google_bp, url_prefix="/login")
app.register_blueprint(main_blueprint)
app.register_blueprint(news_bp)
app.register_blueprint(feedback_bp, url_prefix='/feedback')
app.register_blueprint(gemini_bp)

if __name__ == '__main__':

    with app.app_context():
        try:
            db.create_all()
            create_tags()
            logger.info("Database tables created successfully")
            app.run(debug=False)
        except Exception as e:
            logger.error(f"Database initialization error: {e}")