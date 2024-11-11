from flask import Flask
from models import db
from flask_login import LoginManager
from views import main_blueprint
from auth import auth_blueprint, create_initial_users, login_manager

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'secret keyyyyy'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager.login_view = 'auth.login'
login_manager.init_app(app)


app.register_blueprint(main_blueprint, url_prefix='/')
app.register_blueprint(auth_blueprint, url_prefix='/auth')


with app.app_context():
    db.create_all()
    create_initial_users()

if __name__ == '__main__':
    app.run(debug=True, port=8000)
