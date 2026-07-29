from flask import request, g, jsonify
from functools import wraps
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = URLSafeTimedSerializer(Config.SECRET_KEY).loads(token, max_age=3600)
            current_user = User.query.filter_by(username=data['username']).first()
        except BadSignature:
            return jsonify({'message': 'Token is invalid!'}), 401
        except SignatureExpired:
            return jsonify({'message': 'Token has expired!'}), 401

        g.current_user = current_user
        return f(*args, **kwargs)

    return decorated
