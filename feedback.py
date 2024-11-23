from flask import Blueprint, jsonify, request
from datetime import datetime
from models import db, FeedbackQuestion, Response

# Create a Blueprint
feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/get_active_feedback_question', methods=['GET'])
def get_active_feedback_question():
    """Fetch the currently active feedback question."""
    now = datetime.utcnow()
    question = FeedbackQuestion.query.filter(
        FeedbackQuestion.active_start_date <= now,
        FeedbackQuestion.active_end_date >= now
    ).first()

    if question:
        return jsonify({
            "id": question.id,
            "question_text": question.question_text,
            "question_type": question.question_type
        })
    else:
        return jsonify({"message": "No active feedback question"}), 404

@feedback_bp.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    """Submit feedback provided by the user."""
    data = request.json
    question_id = data.get('question_id')
    user_response = data.get('response')
    additional_feedback = data.get('additional_feedback')

    if not question_id or not user_response:
        return jsonify({"message": "Invalid data"}), 400

    try:
        feedback = Response(
            feedback_id=question_id,
            content=f"{user_response}: {additional_feedback}" if additional_feedback else user_response
        )
        db.session.add(feedback)
        db.session.commit()
        return jsonify({"message": "Feedback submitted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Failed to submit feedback: {str(e)}"}), 500
