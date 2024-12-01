from flask import Blueprint, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from app.models.music_model import MusicModel
import uuid

main = Blueprint('main', __name__)
model = MusicModel()

ALLOWED_EXTENSIONS = {'wav', 'mp3'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and allowed_file(file.filename):
        filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
        filepath = os.path.join('app/static/uploads', filename)
        file.save(filepath)
        
        resultado = model.predecir_genero(filepath)
        
        # Limpiar el archivo después de procesarlo
        os.remove(filepath)
        
        if resultado:
            return render_template('result.html', 
                                resultado=resultado['predicciones'], 
                                espectrogramas=resultado['espectrogramas'])
        else:
            return jsonify({'error': 'Error processing audio file'})
    
    return jsonify({'error': 'Invalid file type'})