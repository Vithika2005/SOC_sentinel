#SentinelX/enterprise/legacy-admin/app/main.py
import os
from flask import Flask
from app.config import Config
from app.database import db
from app.admin import admin_bp
from app.users import users_bp
from app.upload import upload_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(admin_bp)
app.register_blueprint(users_bp)
app.register_blueprint(upload_bp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)