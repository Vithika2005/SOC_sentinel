from flask import request, jsonify
from werkzeug.security import check_password_hash
from ..shared.config import app_config

def login():
    user_data = request.get_json()
    username = user_data['username']
    password = user_data['password']

    # Query the database for the user
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        token = jwt_handler.encode_auth_token(user.id)
        return jsonify({'token': token.decode('UTF-8')})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
