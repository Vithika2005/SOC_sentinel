#SentinelX/enterprise/auth-service/app/main.py
from flask import Flask, jsonify
from app.auth import token_required
from app.database import init_db, db
from app.shared.config import app_config
import app.login as auth_login

app = Flask(__name__)
app.config.from_object(app_config['development'])
init_db(app)

with app.app_context():
    db.create_all()

@app.route('/login', methods=['POST'])
def login():
    return auth_login.login()

@app.route('/protected', methods=['GET'])
@token_required
def protected(current_user):
    return jsonify({'message': f'Hello, {current_user.username}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)