"""
Filename: test_views.py
"""
import pytest
from website import create_app
from flask_login import current_user
from website.models import Student, Food, Tag, Favorites, FeedbackQuestion, Administrator
from website.views import menu_bp


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_dining_experience(client):
    response = client.get('/dining-experience')

    assert response.status_code == 200

def test_team(client):
    response = client.get('/team')
    
    assert response.status_code == 200


def test_menu(client):
    response = client.get('/menu')

    assert response.status_code == 200


def test_contact(client):
    response = client.get('/contact')

    assert response.status_code == 200


def test_userdashboard(client):
    response = client.get('/userdashboard')

    assert response.status_code == 302

def test_admindashboard(client):

    response = client.get('/admin/dashboard')

    assert response.status_code == 302


def test_logout(client):
    response = client.get('/logout')

    assert response.status_code == 302



def test_menu_page(client):
    pass

def test_get_current_menu(client):
    pass

def test_submit_feedback(client):
    pass


def test_get_dining_hall_menu(client):
    pass


# testing apis 
def test_get_weekly_menu(client):
    pass

def test_get_dining_hours(client):
    pass
