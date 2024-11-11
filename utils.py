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
            Tag(name="Vegetarian", type="FoodType"),
            Tag(name="Gluten Free", type="FoodType"),
            Tag(name="Farm to Fork", type="FoodType"),
            Tag(name="Humane", type="FoodType"),
            Tag(name="Organic", type="FoodType")
        ]
        
        db.session.bulk_save_objects(tags)
        db.session.commit()

def filter_foods(selected_tags):
    # Step 1: Retrieve tags matching the selected tags
    selected_tag_names = selected_tags  # Assume these are passed in from the query string or form
    tags = Tag.query.filter(Tag.name.in_(selected_tag_names)).all()

    # Step 2: Query food items that have the selected tags
    foods_query = db.session.query(Food).join(Food.tags).filter(Tag.id.in_([tag.id for tag in tags]))

    # Step 3: Execute the query and get the filtered food items
    filtered_foods = foods_query.all()
    
    return filtered_foods

def get_all_foods():
    # Step 1: Query all food items from the Food table
    foods_query = db.session.query(Food)

    # Step 2: Execute the query to get all food items
    all_foods = foods_query.all()

    return all_foods

