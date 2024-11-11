from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from datetime import datetime
import os
import logging
from dining_predictor import DiningHallPredictor
from models import db, FeedbackQuestion

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

main_blueprint = Blueprint('main', __name__)

# Initialize predictor
base_dir = os.path.dirname(os.path.abspath(__file__))
predictor = None
predictor_initialized = False

def initialize_predictor():
    """Initialize the DiningHallPredictor with models"""
    global predictor, predictor_initialized
    try:
        predictor = DiningHallPredictor(
            model_dir=os.path.join(base_dir, 'ml_models'),
            data_dir=os.path.join(base_dir, 'data')
        )
        
        # Check if we need to train models
        if not any(predictor.models):
            logger.info("No saved models found, training new models...")
            df = predictor.load_data('October-*.csv')
            predictor.train_models(df, save=True)
        
        predictor_initialized = True
        logger.info("Predictor initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize predictor: {str(e)}")
        return False

# Initialize when the blueprint is created
initialize_predictor()

@main_blueprint.route('/')
def index():
    return render_template('index.html')

@main_blueprint.route('/dining-experience')
def dining_experience():
    return render_template('dining_experience.html')

@main_blueprint.route('/team')
def team():
    return render_template('team.html')

@main_blueprint.route('/menu')
def menu():
    return render_template('menu.html')

@main_blueprint.route('/contact')
def contact():
    return render_template('contact.html')

@main_blueprint.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admindashboard.html')

@main_blueprint.route('/admin/feedback-question', methods=['POST'])
def create_feedback_question():
    try:
        question_text = request.form.get('questionText')
        question_type = request.form.get('questionType')
        active_start_date = datetime.strptime(request.form.get('activeStartDate'), '%Y-%m-%d').date()
        active_end_date = datetime.strptime(request.form.get('activeEndDate'), '%Y-%m-%d').date()

        new_question = FeedbackQuestion(
            question_text=question_text,
            question_type=question_type,
            active_start_date=active_start_date,
            active_end_date=active_end_date
        )
        db.session.add(new_question)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Question created successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@main_blueprint.route('/admin/feedback-question/<int:question_id>', methods=['DELETE'])
def delete_feedback_question(question_id):
    try:
        print(f"Attempting to delete question {question_id}")  # Debug log
        question = FeedbackQuestion.query.get_or_404(question_id)
        db.session.delete(question)
        db.session.commit()
        print("Question deleted successfully")  # Debug log
        return jsonify({
            'status': 'success',
            'message': 'Question deleted successfully'
        })
    except Exception as e:
        print(f"Error deleting question: {str(e)}")  # Debug log
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@main_blueprint.route('/api/admin/feedback-questions', methods=['GET'])
def get_feedback_questions():
    try:
        questions = FeedbackQuestion.query.order_by(FeedbackQuestion.created_at.desc()).all()
        return jsonify({
            'status': 'success',
            'questions': [{
                'id': q.id,
                'question_text': q.question_text,
                'question_type': q.question_type,
                'active_start_date': q.active_start_date.isoformat(),
                'active_end_date': q.active_end_date.isoformat(),
                'created_at': q.created_at.isoformat() if q.created_at else None
            } for q in questions]
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@main_blueprint.route('/api/wait-times')
def get_wait_times():
    """API endpoint to get wait time predictions for dining halls"""
    try:
        if not predictor_initialized:
            logger.error("Predictor not properly initialized")
            raise Exception("Prediction service unavailable")

        current_time = datetime.now()
        predictions = {}
        
        # Get predictions for each dining hall
        for location in ['Dana', 'Roberts', 'Foss']:
            try:
                prediction = predictor.predict_wait_times(current_time, location)
                
                if prediction:
                    if prediction.get('status') == 'closed':
                        predictions[location] = {
                            'status': 'closed',
                            'message': prediction['message']
                        }
                    else:
                        predictions[location] = {
                            'crowd': prediction['predicted_count'],
                            'wait_time': prediction['wait_time_minutes'],
                            'status': 'success'
                        }
                else:
                    predictions[location] = {
                        'status': 'error',
                        'message': 'No prediction available'
                    }
                    
            except Exception as e:
                logger.error(f"Error predicting for {location}: {str(e)}")
                predictions[location] = {
                    'status': 'error',
                    'message': 'Temporarily unavailable'
                }
        
        return jsonify({
            'status': 'success',
            'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
            'predictions': predictions
        })
        
    except Exception as e:
        logger.error(f"Error in wait-times endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Service temporarily unavailable',
            'predictions': {
                location: {
                    'status': 'error',
                    'message': 'Temporarily unavailable'
                } for location in ['Dana', 'Roberts', 'Foss']
            }
        }), 500

@main_blueprint.route('/userdashboard')
def userdashboard():
    return render_template('userdashboard.html')