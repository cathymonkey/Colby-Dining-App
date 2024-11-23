import os
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("API_KEY"))

gemini_bp = Blueprint('gemini', __name__)

@gemini_bp.route('/gemini-chat', methods=['POST'])
def gemini_chat():
    user_message = request.form.get('message')
    if user_message:
        try:
            # Use Gemini to generate a response
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(user_message)
            return jsonify({"reply": response.text})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "No message provided"}), 400

