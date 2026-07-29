import os
from werkzeug.utils import secure_filename

def save_file(file):
    if file:
        # Ensure the upload directory exists
        upload_folder = '/path/to/save'
        os.makedirs(upload_folder, exist_ok=True)
        
        # Secure the filename to prevent malicious uploads
        filename = secure_filename(file.filename)
        
        # Save the file to the specified path
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        return f"File {filename} has been uploaded successfully."
    else:
        return "No file part in the request.", 400

def delete_file(filename):
    file_path = '/path/to/save/' + filename
    try:
        os.remove(file_path)
        return f"File {filename} has been deleted successfully."
    except FileNotFoundError:
        return f"File {filename} not found.", 404
