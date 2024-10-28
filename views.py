from flask import Blueprint, render_template, redirect, url_for
from flask import request
from models import db
from flask_login import login_required, current_user

main_blueprint = Blueprint('main', __name__)

