import tensorflow as tf
import numpy as np
import librosa

class AudioPredictor:
    def __init__(self, model_path):
        # Cargar el modelo usando tf.keras directamente
        self.model = tf.keras.models.load_model(model_path)
        
    def extract_features(self, audio_path):
        try:
            # Cargar el audio y extraer características
            y, sr = librosa.load(audio_path, duration=30)
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            mfccs_processed = np.mean(mfccs.T, axis=0)
            return mfccs_processed
        except Exception as e:
            raise Exception(f"Error extracting features: {str(e)}")

    def predict(self, audio_path):
        try:
            # Extraer características
            features = self.extract_features(audio_path)
            
            # Preparar los datos para la predicción
            features = np.expand_dims(features, axis=0)
            
            # Realizar predicción
            predictions = self.model.predict(features)
            
            # Obtener el género predicho y la confianza
            predicted_index = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_index])
            
            return predicted_index, confidence
            
        except Exception as e:
            raise Exception(f"Error during prediction: {str(e)}")
            