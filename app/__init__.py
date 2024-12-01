# app/__init__.py
from flask import Flask
from config import Config
import os
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Asegurarnos de que existe el directorio de uploads
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Configurar límites de tamaño de archivo
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
    
    from app.controllers.routes import main
    app.register_blueprint(main)
    
    return app