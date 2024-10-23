import os
from werkzeug.utils import secure_filename
from config import Config

class AudioService:
    @staticmethod
    def save_audio_file(audio_file):
        if audio_file and AudioService._allowed_file(audio_file.filename):
            filename = secure_filename(audio_file.filename)
            filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
            audio_file.save(filepath)
            return filepath
        raise ValueError("Invalid audio file")

    @staticmethod
    def _allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

    @staticmethod
    def cleanup_file(filepath):
        if os.path.exists(filepath):
            os.remove(filepath)