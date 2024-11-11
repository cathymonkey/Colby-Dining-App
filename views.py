from flask import Blueprint, render_template, jsonify, request, redirect, session, url_for
from flask_login import current_user, login_required
from datetime import datetime
import os
import logging
from auth import admin_required
from dining_predictor import DiningHallPredictor
from models import db, FeedbackQuestion, Administrator

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

# Initialize predictor when blueprint is created
initialize_predictor()

@main_blueprint.context_processor
def inject_user():
    """Make current_user available to all templates"""
    return dict(current_user=current_user)

# Basic routes
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

# Dashboard routes
@main_blueprint.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    return render_template('admindashboard.html')

@main_blueprint.route('/userdashboard')
@login_required
def userdashboard():
    if isinstance(current_user, Administrator):
        return redirect(url_for('main.admin_dashboard'))
    return render_template('userdashboard.html')

# Feedback question routes
@main_blueprint.route('/admin/feedback-question', methods=['POST'])
@login_required
@admin_required
def create_feedback_question():
    try:
        new_question = FeedbackQuestion(
            question_text=request.form.get('questionText'),
            question_type=request.form.get('questionType'),
            active_start_date=datetime.strptime(request.form.get('activeStartDate'), '%Y-%m-%d').date(),
            active_end_date=datetime.strptime(request.form.get('activeEndDate'), '%Y-%m-%d').date(),
            administrator_id=current_user.admin_email
        )
        db.session.add(new_question)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Question created successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400

@main_blueprint.route('/admin/feedback-question/<int:question_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_feedback_question(question_id):
    try:
        question = FeedbackQuestion.query.get_or_404(question_id)
        if question.administrator_id != current_user.admin_email:
            return jsonify({'status': 'error', 'message': 'Unauthorized to delete this question'}), 403
        
        db.session.delete(question)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Question deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400

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
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Wait times API
@main_blueprint.route('/api/wait-times')
def get_wait_times():
    """Get wait time predictions for dining halls"""
    try:
        if not predictor_initialized:
            logger.error("Predictor not properly initialized")
            raise Exception("Prediction service unavailable")

        current_time = datetime.now()
        predictions = {}
        
        for location in ['Dana', 'Roberts', 'Foss']:
            try:
                prediction = predictor.predict_wait_times(current_time, location)
                if prediction:
                    predictions[location] = {
                        'status': 'closed' if prediction.get('status') == 'closed' else 'success',
                        'message': prediction.get('message', None),
                        'crowd': prediction.get('predicted_count', None),
                        'wait_time': prediction.get('wait_time_minutes', None)
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
            'predictions': {location: {'status': 'error', 'message': 'Temporarily unavailable'} 
                          for location in ['Dana', 'Roberts', 'Foss']}
        }), 500
    
@main_blueprint.route('/userdashboard')
@login_required
def user_dashboard():
    return render_template('userdashboard.html')

@main_blueprint.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('main.index'))