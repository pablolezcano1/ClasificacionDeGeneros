# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-12345'
    UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # Aumentado a 50MB
    # Agregamos estas configuraciones
    MAX_CONTENT_PATH = None
    UPLOAD_EXTENSIONS = ['.wav']