from flask import Blueprint, render_template, redirect, url_for
from flask import request
from models import db
from flask_login import login_required, current_user

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():
    return render_template('index.html')

@main_blueprint.route('/menu')
def menu():
    return render_template('menu.html')

@main_blueprint.route('/contact')
def contact():
    return render_template('contact.html')

@main_blueprint.route('/userdashboard')
#@login_required 
#Comment out for Google OAuth implement
def userdashboard():
    return render_template('userdashboard.html')