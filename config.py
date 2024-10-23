import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = 'tu_clave_secreta'
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MODEL_PATH = os.path.join(BASE_DIR, 'modelos', 'modelo_entrenado_6.h5')
    ALLOWED_EXTENSIONS = {'wav', 'mp3'}
    GENRES = ['blues', 'classical', 'country', 'disco', 'hiphop', 
              'jazz', 'metal', 'pop', 'reggae', 'rock']

    @staticmethod
    def init_app(app):
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)