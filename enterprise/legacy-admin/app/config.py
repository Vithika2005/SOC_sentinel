#SentinelX/enterprise/legacy-admin/app/config.py
import os

class Config:
    # Flagged by Gitleaks / Secret Scanners
    SECRET_KEY = "you-will-never-guess-hardcoded-secret-key"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:////app/data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False