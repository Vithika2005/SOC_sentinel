import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:////app/api_service.db')

class DevelopmentConfig(Config):
    DEBUG = True

app_config = {
    'development': DevelopmentConfig
}