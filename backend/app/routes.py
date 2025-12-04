from flask import request, Blueprint, jsonify
from .llama_service import ask_emergency, ask_health_assistant

api = Blueprint('api', __name__)

@api.route('/ask-ai', methods=["POST"])
def ask_ai():
    data = request.json
    user_question = data.get("question")
    category =  data.get("category")
    age = data.get("age")

    if category.lower() == "emergency":
        response = ask_emergency(user_question, age)
    else:
        response = ask_health_assistant(user_question, category, age)

    return jsonify({"answer": response})