from flask import Blueprint, render_template, jsonify
from datetime import datetime
import os
import logging
from flask import Blueprint, render_template
from flask_login import login_required

# from dining_predictor import DiningHallPredictor

import pathlib

import requests
from flask import Flask, session, abort, redirect, request
from flask import render_template


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

main_blueprint = Blueprint('main', __name__)

# Initialize predictor
base_dir = os.path.dirname(os.path.abspath(__file__))
predictor = None
predictor_initialized = False

# def initialize_predictor():
#     """Initialize the DiningHallPredictor with models"""
#     global predictor, predictor_initialized
#     try:
#         predictor = DiningHallPredictor(
#         model_dir=os.path.join(base_dir, 'ml_models'),
#         data_dir=os.path.join(base_dir, 'data')
#     )
#
#         # Check if we need to train models
#         if not any(predictor.models):
#             logger.info("No saved models found, training new models...")
#             df = predictor.load_data('October-*.csv')
#             predictor.train_models(df, save=True)
#
#         predictor_initialized = True
#         logger.info("Predictor initialized successfully")
#         return True
#     except Exception as e:
#         logger.error(f"Failed to initialize predictor: {str(e)}")
#         return False

# Initialize when the blueprint is created
# initialize_predictor()

@main_blueprint.route('/')
def index():
    return render_template('index.html')

@main_blueprint.route('/about')
def about():
    return render_template('about.html')

@main_blueprint.route('/menu')
def menu():
    return render_template('menu.html')

@main_blueprint.route('/contact')
def contact():
    return render_template('contact.html')

@main_blueprint.route('/userdashboard')
@login_required
def userdashboard():

    return render_template('userdashboard.html')


# @main_blueprint.route('/api/wait-times')
# def get_wait_times():
#     """API endpoint to get wait time predictions for dining halls"""
#     try:
#         if not predictor_initialized:
#             logger.error("Predictor not properly initialized")
#             raise Exception("Prediction service unavailable")
#
#         current_time = datetime.now()
#         predictions = {}
#
#         # Get predictions for each dining hall
#         for location in ['Dana', 'Roberts', 'Foss']:
#             try:
#                 # Use the correct method name here
#                 prediction = predictor.predict_wait_times(current_time, location)  # Make sure this matches your class method name
#
#                 if prediction:
#                     if prediction.get('status') == 'closed':
#                         predictions[location] = {
#                             'status': 'closed',
#                             'message': prediction['message']
#                         }
#                     else:
#                         predictions[location] = {
#                             'crowd': prediction['predicted_count'],
#                             'wait_time': prediction['wait_time_minutes'],
#                             'status': 'success'
#                         }
#                 else:
#                     predictions[location] = {
#                         'status': 'error',
#                         'message': 'No prediction available'
#                     }
#
#             except Exception as e:
#                 logger.error(f"Error predicting for {location}: {str(e)}")
#                 predictions[location] = {
#                     'status': 'error',
#                     'message': 'Temporarily unavailable'
#                 }
#
#         return jsonify({
#             'status': 'success',
#             'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
#             'predictions': predictions
#         })
#
#     except Exception as e:
#         logger.error(f"Error in wait-times endpoint: {str(e)}")
#         return jsonify({
#             'status': 'error',
#             'message': 'Service temporarily unavailable',
#             'predictions': {
#                 location: {
#                     'status': 'error',
#                     'message': 'Temporarily unavailable'
#                 } for location in ['Dana', 'Roberts', 'Foss']
#             }
#         }), 500




@main_blueprint.route('/', endpoint='main_index')
def index():
    return render_template('index.html')

@main_blueprint.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    feedback_data = request.json  # Get the JSON data sent by the frontend
    # Here you can add code to process feedback, e.g., save to database or log it.
    return jsonify({"status": "success"}), 200



