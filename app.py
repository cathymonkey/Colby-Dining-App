from flask import Flask
from models import db, DiningHall, Food, MealSchedule
from flask_login import LoginManager
from views import main_blueprint
from datetime import time

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
        
        # Hard coding food item for testing
        # Check if Dana dining hall already exists
        dana_hall = DiningHall.query.filter_by(name="Dana").first()
        if not dana_hall:
            # Create Dana dining hall
            dana_hall = DiningHall(name="Dana")
            db.session.add(dana_hall)
            db.session.commit()  # Commit so we can use dana_hall.id

        # Add Food items for Dana
        food_item_1 = Food(
            name="Beef Ramen",
            description="A savory beef ramen with vegetables and a boiled egg.",
            label="Entree",
            calories=550,
            dining_hall_id=dana_hall.id  # Link to Dana
        )

        food_item_2 = Food(
            name="Vegan Salad",
            description="A fresh salad with mixed greens, cherry tomatoes, and a light vinaigrette.",
            label="Salad",
            calories=200,
            dining_hall_id=dana_hall.id  # Link to Dana
        )

        db.session.add_all([food_item_1, food_item_2])
        
        # Add a MealSchedule entry for Dana
        schedule = MealSchedule(
            dining_hall_id=dana_hall.id,  # Link to Dana
            meal_type="Lunch",
            start_time=time(11, 30),  # 11:30 AM
            end_time=time(14, 0)      # 2:00 PM
        )
        
        db.session.add(schedule)
        db.session.commit()  # Commit all changes




    app.run(debug=True, port=8000)