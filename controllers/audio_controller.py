from flask import request, jsonify
from config import Config
import librosa  # Librería para el procesamiento de audio
import numpy as np
import tensorflow as tf

class AudioController:
    def __init__(self):
        self.model = tf.keras.models.load_model(Config.MODEL_PATH)
        self.genres = Config.GENRES

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

    def handle_prediction(self):
        if 'audio' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['audio']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file and self.allowed_file(file.filename):
            try:
                # Cargar archivo con librosa
                y, sr = librosa.load(file, sr=None)
                # Procesar audio para predecir (Ejemplo básico de extracción de características)
                mfcc = librosa.feature.mfcc(y, sr=sr, n_mfcc=13)
                mfcc_mean = np.mean(mfcc, axis=1).reshape(1, -1)
                prediction = self.model.predict(mfcc_mean)
                predicted_genre = self.genres[np.argmax(prediction)]

                return jsonify({
                    'genre': predicted_genre,
                    'confidence': float(np.max(prediction) * 100)
                }), 200

            except Exception as e:
                return jsonify({'error': str(e)}), 500

        return jsonify({'error': 'Invalid file type'}), 400
