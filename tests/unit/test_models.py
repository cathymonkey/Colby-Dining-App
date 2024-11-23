from website.models import User, Food, Tag, food_tags, FeedbackQuestion, Administrator

def test_user_set_password():
 user = User()
 user.set_password('password')
 assert user.password_hash is not None
 assert user.password_hash != 'password'

 