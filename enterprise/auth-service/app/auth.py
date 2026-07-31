#SentinelX/enterprise/auth-service/app/auth.py
from flask import request, jsonify
from functools import wraps
import jwt
from app.models import User
from app.shared.config import Config

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
            else:
                token = auth_header

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            user_id = data['sub']
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 401

        current_user = User.query.filter_by(id=user_id).first()
        if not current_user:
            return jsonify({'message': 'User not found!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated
