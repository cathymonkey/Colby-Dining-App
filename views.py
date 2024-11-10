from flask import Blueprint, render_template, redirect, url_for
from flask import request
from models import db, Food, Tag, food_tags
from flask_login import login_required, current_user


main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():
    # Fetching the tags for dining halls
    dana_tag = Tag.query.filter_by(name="Dana", type="Location").first()
    roberts_tag = Tag.query.filter_by(name="Roberts", type="Location").first()
    foss_tag = Tag.query.filter_by(name="Foss", type="Location").first()

    # Fetching food items associated with each dining hall tag
    dana_food_items = Food.query \
        .join(food_tags) \
        .join(Tag) \
        .filter(Tag.id == dana_tag.id) \
        .all()

    roberts_food_items = Food.query \
        .join(food_tags) \
        .join(Tag) \
        .filter(Tag.id == roberts_tag.id) \
        .all()

    foss_food_items = Food.query \
        .join(food_tags) \
        .join(Tag) \
        .filter(Tag.id == foss_tag.id) \
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