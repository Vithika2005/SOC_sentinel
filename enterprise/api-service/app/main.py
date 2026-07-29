from flask import Flask
from app.users import create_user
from app.orders import create_order
from app.upload import upload_file
from app.reports import get_reports
from app.database import init_db
from app.shared.config import app_config

app = Flask(__name__)
app.config.from_object(app_config['development'])
init_db(app)

@app.route('/users', methods=['POST'])
def users():
    return create_user()

@app.route('/orders', methods=['POST'])
def orders():
    return create_order()

@app.route('/upload', methods=['POST'])
def upload():
    return upload_file()

@app.route('/reports', methods=['GET'])
def reports():
    return get_reports()
