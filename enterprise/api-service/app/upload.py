from flask import request, jsonify
from app.auth import token_required

@token_required
def upload_file(current_user):
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file:
        file.save('/tmp/' + file.filename)
        return jsonify({'message': 'File uploaded successfully'}), 201