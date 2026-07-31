#SentinelX/enterprise/legacy-admin/app/users.py
from flask import Blueprint, request, jsonify
from sqlalchemy import text
from app.database import db

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    username = data.get('username', '')
    password = data.get('password', '')

    if not username or not password:
        return jsonify({'message': 'Username and password required'}), 400

    # SQL Injection flaw (Flagged by SAST)
    query = f"INSERT INTO user (username, password) VALUES ('{username}', '{password}')"
    
    try:
        db.session.execute(text(query))
        db.session.commit()
        return jsonify({'message': f'User {username} created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'executed_query': query}), 500

@users_bp.route('/users', methods=['GET'])
def get_users():
    return jsonify({'users': [{'id': 1, 'username': 'admin'}]}), 200