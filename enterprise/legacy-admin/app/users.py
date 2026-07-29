from flask import request, jsonify
from app.auth import token_required

@app.route('/users', methods=['POST'])
@token_required
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    # Here you would typically save the user to the database
    # For demonstration, we'll just return a success message
    return jsonify({'message': f'User {username} created successfully'}), 201

@app.route('/users', methods=['GET'])
@token_required
def get_users():
    # Here you would typically fetch users from the database
    # For demonstration, we'll just return a list of dummy users
    users = [
        {'id': 1, 'username': 'user1'},
        {'id': 2, 'username': 'user2'}
    ]
    return jsonify({'users': users}), 200
