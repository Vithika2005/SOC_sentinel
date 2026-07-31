from flask import request, jsonify
from app.database import db
from app.models import User

def create_user():
    user_data = request.get_json()
    new_user = User(username=user_data['username'], password=user_data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201