from flask import Blueprint, render_template, redirect, url_for
from flask import request
from models import db, DiningHall, Food, MealSchedule
from flask_login import login_required, current_user


main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():
    # Fetching the dining halls
    dana_hall = DiningHall.query.filter_by(name="Dana").first()
    roberts_hall = DiningHall.query.filter_by(name="Roberts").first()
    foss_hall = DiningHall.query.filter_by(name="Foss").first()

    # Updated queries with explicit join conditions
    dana_food_items = Food.query \
        .select_from(Food) \
        .join(MealSchedule, MealSchedule.dining_hall_id == Food.dining_hall_id) \
        .filter(MealSchedule.dining_hall == dana_hall) \
        .all()

    roberts_food_items = Food.query \
        .select_from(Food) \
        .join(MealSchedule, MealSchedule.dining_hall_id == Food.dining_hall_id) \
        .filter(MealSchedule.dining_hall == roberts_hall) \
        .all()

    foss_food_items = Food.query \
        .select_from(Food) \
        .join(MealSchedule, MealSchedule.dining_hall_id == Food.dining_hall_id) \
        .filter(MealSchedule.dining_hall == foss_hall) \
        .all()

    # Rendering the template
    return render_template('index.html', 
                           dana_food_items=dana_food_items, 
                           roberts_food_items=roberts_food_items, 
                           foss_food_items=foss_food_items)

@main_blueprint.route('/about')
def about():
    return render_template('about.html')

@main_blueprint.route('/menu')
def menu():
    return render_template('menu.html')

@main_blueprint.route('/contact')
def contact():
    return render_template('contact.html')

@main_blueprint.route('/userdashboard')
#@login_required 
def userdashboard():
    return render_template('userdashboard.html')