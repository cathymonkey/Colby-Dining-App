from datetime import datetime
from .models import MealSchedule

def get_current_meal(dining_hall):
    current_time = datetime.now().time()
    
    # Query for the meal schedules for the current dining hall
    current_schedule = MealSchedule.query.filter(
        MealSchedule.dining_hall_id == dining_hall.id
    ).all()

    # Check which meal period the current time falls into
    for schedule in current_schedule:
        if schedule.start_time <= current_time < schedule.end_time:
            return schedule.meal_type

    return None  # If no meal period matches the current time
