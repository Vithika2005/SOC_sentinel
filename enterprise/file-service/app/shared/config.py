import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'super-secret-key')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/app/uploads')

class DevelopmentConfig(Config):
    DEBUG = True

app_config = {
    'development': DevelopmentConfig
}