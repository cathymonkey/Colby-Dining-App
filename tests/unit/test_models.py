import pytest
from website.models import Student, Food, Tag, Favorites, FeedbackQuestion, Administrator
import datetime

@pytest.fixture
def student():
    return Student(
        student_email='student@colby.edu',
        student_access_token='12345678'
    )

@pytest.fixture
def food_with_tags():
    tag1 = Tag(name='Lunch', type='Meal')
    tag2 = Tag(name='Vegetarian', type='Diet')
    food = Food(name='Salad', description='A healthy salad', calories=200)
    food.tags.extend([tag1, tag2])
    return food, tag1, tag2

@pytest.fixture
def favorite(student, food_with_tags):
    food, _, _ = food_with_tags
    favorite = Favorites(
        student_email=student.student_email,
        food_id=food.id,
        created_at='2024-11-22',
        update_at='2024-11-22'
    )
    return favorite, student, food

@pytest.fixture
def administrator():
    return Administrator(
        admin_email='admin@colby.edu',
        password_hashed='hashedpassword',
        google_id='googleid123',
        fullname='Admin Fullname',
        given_name='Admin',
        family_name='User',
        picture='http://example.com/picture.jpg',
        created_at=datetime.datetime.utcnow(),
        last_login=datetime.datetime.utcnow()
    )

@pytest.fixture
def feedback_question(administrator):
    # Create the FeedbackQuestion instance
    feedback_question = FeedbackQuestion(
        administrator_id=administrator.admin_email,
        question_text='How was your experience?',
        question_type='Text',
        active_start_date=datetime.date(2024, 1, 1),
        active_end_date=datetime.date(2024, 12, 31),
        created_at=datetime.datetime.utcnow()
    )

    administrator.feedback_questions.append(feedback_question)

    return feedback_question, administrator


# Test Student
def test_student_get_id(student):
    assert student.get_id() == 'student@colby.edu'

def test_student_is_authenticated(student):
    assert student.is_authenticated() is True

def test_student_is_active(student):
    assert student.is_active() is True

def test_student_is_anonymous(student):
    assert student.is_anonymous() is False

# Test Food and Tag Association
def test_food_tags_association(food_with_tags):
    food, tag1, tag2 = food_with_tags
    assert tag1 in food.tags
    assert tag2 in food.tags
    assert food in tag1.foods
    assert food in tag2.foods
    assert len(food.tags) == 2

# Test Favorites
def test_favorite_association(favorite):
    favorite_obj, student, food = favorite
    assert favorite_obj.student_email == student.student_email
    assert favorite_obj.food_id == food.id

# Test Admin
def test_administrator_get_id(administrator):
    assert administrator.get_id() == 'admin@colby.edu'

def test_administrator_repr(administrator):
    assert repr(administrator) == '<Administrator admin@colby.edu>'

def test_administrator_feedback_question_association(feedback_question):
    feedback_question_obj, administrator = feedback_question

    assert feedback_question_obj.administrator_id == administrator.admin_email
    assert feedback_question_obj in administrator.feedback_questions
    assert feedback_question_obj.administrator == administrator

