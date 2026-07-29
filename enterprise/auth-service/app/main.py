from flask import Flask, request, jsonify
from app.auth import token_required
from app.models import User
from app.database import init_db
from app.shared.config import app_config

app = Flask(__name__)
app.config.from_object(app_config['development'])
init_db(app)

@app.route('/login', methods=['POST'])
def login():
    return auth.login()

@app.route('/protected', methods=['GET'])
@token_required
def protected(current_user):
    return jsonify({'message': 'Hello, {}'.format(current_user.username)})
