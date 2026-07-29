from flask import request, jsonify
from app.auth import token_required
from app.models import User
from app.database import init_db
from app.shared.config import app_config

app = Flask(__name__)
app.config.from_object(app_config['development'])
init_db(app)

@app.route('/users', methods=['POST'])
@token_required
def create_user(current_user):
    user_data = request.get_json()
    new_user = User(username=user_data['username'], password=user_data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201
