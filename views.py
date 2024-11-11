from flask import Blueprint, render_template, redirect, url_for
from flask import request
from models import db, Food, Tag, food_tags
from flask_login import login_required, current_user
from utils import filter_foods, get_all_foods


main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():

    # Rendering the template
    return render_template('index.html')


@main_blueprint.route('/about')
def about():
    return render_template('about.html')



@main_blueprint.route('/menu', methods=['GET'])
def menu():
    # Get the selected tags from the query parameters
    selected_tags = request.args.getlist('tags')  # List of tags selected by the user

    # If no tags are selected, return all foods
    if not selected_tags:
        filtered_foods = get_all_foods()  # Fetch all food items
    else:
        filtered_foods = filter_foods(selected_tags)  # Filter foods based on selected tags

    # Pass the filtered food items and selected tags to the template
    return render_template('menu.html', foods=filtered_foods, selected_tags=selected_tags)



@main_blueprint.route('/contact')
def contact():
    return render_template('contact.html')

@main_blueprint.route('/userdashboard')
#@login_required 
def userdashboard():
    return render_template('userdashboard.html')

