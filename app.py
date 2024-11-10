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
        
        dana_tag = Tag.query.filter_by(name="Dana", type="Location").first()
        lunch_tag = Tag.query.filter_by(name="Lunch", type="Meal").first()

        if not dana_tag or not lunch_tag:
            raise ValueError("One or more tags are missing")

        # Create Food items and associate them with tags for "Dana" and "Lunch"
        food_item_1 = Food(
            name="Beef Ramen",
            description="A savory beef ramen with vegetables and a boiled egg.",
            label="Entree",
            calories=550
        )

        food_item_2 = Food(
            name="Vegan Salad",
            description="A fresh salad with mixed greens, cherry tomatoes, and a light vinaigrette.",
            label="Salad",
            calories=200
        )

        # Associate each food item with the "Dana" location tag and the "Lunch" meal tag
        food_item_1.tags.extend([dana_tag, lunch_tag])
        food_item_2.tags.extend([dana_tag, lunch_tag])

        # Add the food items to the session
        db.session.add_all([food_item_1, food_item_2])
        db.session.commit()




    app.run(debug=True, port=8000)