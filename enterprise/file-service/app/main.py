from flask import Flask
from app.upload import upload_file
from app.download import download_file

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    return upload_file()

@app.route('/download/<filename>', methods=['GET'])
@token_required
def download(filename):
    return download_file(current_user, filename)
