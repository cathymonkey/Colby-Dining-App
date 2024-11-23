import pytest
from website import create_app, db
from website.models import Administrator, Student
from flask_login import login_user, current_user, logout_user
import os

@pytest.fixture(scope='module')
def test_app():
    """Create a Flask app configured for testing"""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,  
        'SECRET_KEY': 'test-secret-key'
    })
    return app

@pytest.fixture(scope='module')
def test_client(test_app):
    """Create a test client"""
    with test_app.test_client() as testing_client:
        with test_app.app_context():
            yield testing_client

@pytest.fixture(scope='module')
def init_database(test_app):
    """Initialize test database with sample users"""
    with test_app.app_context():
        db.create_all()

        # Create test admin
        admin = Administrator(
            admin_email='admin@colby.edu',
            password_hashed='pbkdf2:sha256:260000$test_hash',
            google_id='test_google_id',
            fullname='Test Admin',
            given_name='Test',
            family_name='Admin'
        )
        admin.set_password('test_password')

        # Create test student
        student = Student(
            student_email='student@colby.edu',
            student_access_token='test_token'
        )

        db.session.add(admin)
        db.session.add(student)
        db.session.commit()

        yield db  

        db.drop_all()

@pytest.fixture(scope='function')
def logged_in_admin(test_client, init_database):
    """Create a logged-in admin session"""
    test_client.post('/login', 
        data={
            'email': 'admin@colby.edu',
            'password': 'test_password'
        },
        follow_redirects=True
    )
    yield test_client
    # Log out after the test
    test_client.get('/logout', follow_redirects=True)

@pytest.fixture(scope='function')
def logged_in_student(test_client, init_database):
    """Create a logged-in student session"""
    with test_client.session_transaction() as sess:
        # Simulate Google OAuth login for student
        sess['student_email'] = 'student@colby.edu'
        sess['google_name'] = 'Test Student'
    yield test_client
    # Clean up session after test
    with test_client.session_transaction() as sess:
        sess.clear()