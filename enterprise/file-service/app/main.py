#SentinelX/enterprise/file-service/app/main.py
import os
from flask import Flask
from app.upload import upload_file
from app.download import download_file
from app.shared.config import app_config, Config

app = Flask(__name__)
app.config.from_object(app_config['development'])

os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    return upload_file()

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    return download_file(filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)