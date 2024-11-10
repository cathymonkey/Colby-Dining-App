from models import db, Tag, Food

def create_tags():
    if Tag.query.count() == 0:  # Check if tags already exist
        tags = [
            Tag(name="Dana", type="Location"),
            Tag(name="Roberts", type="Location"),
            Tag(name="Foss", type="Location"),
            Tag(name="Breakfast", type="Meal"),
            Tag(name="Lunch", type="Meal"),
            Tag(name="Dinner", type="Meal"),
            Tag(name="Vegan", type="FoodType"),
            Tag(name="Gluten-Free", type="FoodType"),
            Tag(name="Vegetarian", type="FoodType")
        ]
        
        db.session.bulk_save_objects(tags)
        db.session.commit()


