<<<<<<< HEAD
from flask import Blueprint, render_template, redirect, url_for
from flask import request
from models import db, Food, Tag, food_tags
from flask_login import login_required, current_user
from utils import filter_foods, get_all_foods

=======
from flask import Blueprint, render_template, jsonify
from datetime import datetime
import os
import logging
from dining_predictor import DiningHallPredictor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
>>>>>>> ff9afb93d6000b7c719b7210cbeb776b20457887

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

    # Rendering the template
    return render_template('index.html')

<<<<<<< HEAD

@main_blueprint.route('/about')
def about():
    return render_template('about.html')
=======
@main_blueprint.route('/dining-experience')
def dining_experience():
    return render_template('dining_experience.html')

@main_blueprint.route('/team')
def team():
    return render_template('team.html')
>>>>>>> ff9afb93d6000b7c719b7210cbeb776b20457887



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
def userdashboard():
    return render_template('userdashboard.html')

<<<<<<< HEAD
=======
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
                # Use the correct method name here
                prediction = predictor.predict_wait_times(current_time, location)  # Make sure this matches your class method name
                
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
>>>>>>> ff9afb93d6000b7c719b7210cbeb776b20457887
