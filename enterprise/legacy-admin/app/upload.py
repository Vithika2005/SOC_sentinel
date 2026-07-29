from flask import request, jsonify
from app.auth import token_required

@app.route('/upload', methods=['POST'])
@token_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file:
        # Save the file to a directory
        file.save('/path/to/save/' + file.filename)
        return jsonify({'message': 'File uploaded successfully'}), 201
