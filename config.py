import os
from datetime import timedelta

class Config:
    # General
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig:
    # Production Only
    REMEMBER_COOKIE_DURATION = timedelta(days=14)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class DevelopmentConfig:
    # Development Locally
    REMEMBER_COOKIE_DURATION = timedelta(seconds=300)
    SQLALCHEMY_DATABASE_URI = "sqlite:///memory"
