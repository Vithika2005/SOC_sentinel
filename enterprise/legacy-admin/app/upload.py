#SentinelX/enterprise/legacy-admin/app/upload.py
import os
from flask import Blueprint, request, jsonify

upload_bp = Blueprint('upload', __name__)
UPLOAD_FOLDER = '/app/uploads'

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    # Path Traversal flaw (Flagged by SAST)
    target_path = os.path.join(UPLOAD_FOLDER, file.filename)
    
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    file.save(target_path)
    
    return jsonify({'message': f'File uploaded successfully to {target_path}'}), 201