import librosa
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import io
import base64

class MusicModel:
    def __init__(self):
        self.generos = [
            "Blues", "Classical", "Country", "Disco", "Hip-Hop",
            "Jazz", "Metal", "Pop", "Reggae", "Rock"
        ]
        self.modelo = tf.keras.models.load_model("app/models/modelo_entrenado_6.h5")
    
    def extraer_caracteristicas(self, audio_path, sr=22050, n_mfcc=13, offset=30):
        try:
            audio, sample_rate = librosa.load(audio_path, sr=sr, offset=offset)
            mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=n_mfcc)
            mfccs_mean = np.mean(mfccs.T, axis=0)
            return mfccs_mean, audio, sample_rate
        except Exception as e:
            print(f"Error al procesar el audio: {e}")
            return None, None, None

    def generar_espectrogramas(self, audio, sr):
        resultados = {}
    
        # Espectrograma MEL
        mel_spect = librosa.feature.melspectrogram(y=audio, sr=sr)
        mel_spect_db = librosa.power_to_db(mel_spect, ref=np.max)
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(mel_spect_db, sr=sr, x_axis='time', y_axis='mel')
        plt.colorbar(format='%+2.0f dB')
        plt.title('Espectrograma MEL')
        
        # Convertir a imagen base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        resultados['mel'] = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close('all')  # Cierra todas las figuras abiertas

        # MFCC
        mfccs = librosa.feature.mfcc(y=audio, sr=sr)
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(mfccs, sr=sr, x_axis='time')
        plt.colorbar(format='%+2.0f')
        plt.title('MFCC')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        resultados['mfcc'] = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close('all')  # Cierra todas las figuras abiertas

        return resultados

    def predecir_genero(self, audio_path):

        caracteristicas, audio, sr = self.extraer_caracteristicas(audio_path, offset=50)
        if caracteristicas is None:
            return None
            
        caracteristicas = np.expand_dims(caracteristicas, axis=0)
        prediccion = self.modelo.predict(caracteristicas)
        
        # Obtener las top 3 predicciones
        top_indices = np.argsort(prediccion[0])[-3:][::-1]
        resultados = []
        for idx in top_indices:
            resultados.append({
                'genero': self.generos[idx],
                'probabilidad': float(prediccion[0][idx] * 100)
            })
        
        # Generar espectrogramas
        espectrogramas = self.generar_espectrogramas(audio, sr)
        
        return {
            'predicciones': resultados,
            'espectrogramas': espectrogramas
        }