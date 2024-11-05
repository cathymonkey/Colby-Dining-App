from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


db = SQLAlchemy()

class Student(db.Model):
    student_email = db.Column(db.String(255), primary_key = True)
    student_access_token = db.Column(db.String(255), unique = True, nullable = False)
    fav = db.relationship('Favorites', backref = 'student')

class Food(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    description = db.Column(db.Text)
    label = db.Column(db.String(255))
    calories = db.Column(db.Integer)
    fav = db.relationship('Favorites', backref = 'food')

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    created_at = db.Column(db.Date, nullable = False)
    update_at = db.Column(db.Date, nullable = False)
    student_email = db.Column(db.String(255), db.ForeignKey('student.student_email'), nullable = False)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable = False)

class Administrator(db.Model):
    admin_email = db.Column(db.String(255), primary_key = True)
    password_hashed = db.Column(db.String(128), nullable = False)
    feedback = db.relationship('Feedback', backref = 'administrator')

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    admin_email = db.Column(db.String(255), db.ForeignKey('administrator.admin_email'), nullable = False)
    content = db.Column(db.Text, nullable = False)
    num_responses = db.Column(db.Integer)
    created_at = db.Column(db.Date, nullable = False)
    update_at = db.Column(db.Date, nullable = False)
    response = db.relationship('Response', backref = 'feedback')

class Response(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text, nullable = False)
    feedback_id = db.Column(db.Integer, db.ForeignKey('feedback.id'), nullable = False)

class WaitTime(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    location = db.Column(db.String(255), nullable = False)
    num_swipes = db.Column(db.Integer)
    start_time = db.Column(db.Time, nullable = False)
    end_time = db.Column(db.Time, nullable = False)
    date = db.Column(db.Date, nullable = False)
    day_of_week = db.Column(db.Integer, nullable = False)
    predicted_wait = db.Column(db.Integer, nullable = False)
