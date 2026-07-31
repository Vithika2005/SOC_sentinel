#SentinelX/enterprise/auth-service/app/login.py
from flask import request, jsonify
from werkzeug.security import check_password_hash
from app.models import User
import app.jwt_handler as jwt_handler

def login():
    user_data = request.get_json() or {}
    username = user_data.get('username')
    password = user_data.get('password')

    if not username or not password:
        return jsonify({'message': 'Invalid credentials'}), 401

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        token = jwt_handler.encode_auth_token(user.id)
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
