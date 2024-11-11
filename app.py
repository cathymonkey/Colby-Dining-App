from flask import Flask
from models import db
from flask_login import LoginManager
from views import main_blueprint
from auth import auth_blueprint, create_initial_users, login_manager  # Import login_manager

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'secret keyyyyy'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# Register blueprints for routes
app.register_blueprint(main_blueprint, url_prefix='/')       # Main site routes
app.register_blueprint(auth_blueprint, url_prefix='/auth')   # Authentication routes

# Run the initial user creation function on app startup
with app.app_context():
    db.create_all()  # Create tables (if they don't already exist)
    create_initial_users()  # Add initial users if they don't exist

if __name__ == '__main__':
    app.run(debug=True, port=8000)
