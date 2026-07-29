from flask import Flask, request
from functools import wraps
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app_config.SECRET_KEY)
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        current_user = User.query.filter_by(id=data['id']).first()
        return f(current_user, *args, **kwargs)

    return decorated
