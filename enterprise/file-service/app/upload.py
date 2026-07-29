from flask import request, jsonify
from app.auth import token_required
from app.database import init_db
from app.shared.config import app_config

app = Flask(__name__)
app.config.from_object(app_config['development'])
init_db(app)

@app.route('/upload', methods=['POST'])
@token_required
def upload_file(current_user):
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file:
        # Save the file to a directory
        file.save('/path/to/save/' + file.filename)
        return jsonify({'message': 'File uploaded successfully'}), 201
