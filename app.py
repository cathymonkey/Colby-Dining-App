from flask import Flask
from models import db, Food, Tag, food_tags
from flask_login import LoginManager
from views import main_blueprint
from datetime import time
from utils import create_tags


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret keyyyyy'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

#login_manager = LoginManager(app)

# Register blueprint for routes
app.register_blueprint(main_blueprint)


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()  # Create tables (if not created)

        create_tags()


    app.run(debug=True, port=8000)