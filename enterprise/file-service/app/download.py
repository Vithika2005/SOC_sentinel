from flask import send_file, abort
from app.auth import token_required
from app.database import init_db
from app.shared.config import app_config

app = Flask(__name__)
app.config.from_object(app_config['development'])
init_db(app)

@app.route('/download/<filename>', methods=['GET'])
@token_required
def download_file(current_user, filename):
    try:
        # Construct the file path based on the filename
        file_path = '/path/to/save/' + filename
        
        # Send the file for download
        return send_file(file_path)
    
    except FileNotFoundError:
        abort(404)
