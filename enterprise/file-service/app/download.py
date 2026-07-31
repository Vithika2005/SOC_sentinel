#SentinelX/enterprise/file-service/app/download.py
import os
from flask import send_from_directory, abort, jsonify
from app.auth import token_required
from app.shared.config import Config

UPLOAD_FOLDER = Config.UPLOAD_FOLDER

@token_required
def download_file(current_user, filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'message': 'File not found'}), 404