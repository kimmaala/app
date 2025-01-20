from flask import request, jsonify
from app import app
from app.services import UserService


@app.route('/')
def hello():
    return ("hello world!")

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user_service = UserService()
    response, status = user_service.register_user(data)
    return jsonify(response), status

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_service = UserService()
    response, status = user_service.login_user(data)
    return jsonify(response), status





    
