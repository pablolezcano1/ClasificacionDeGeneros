from flask import Flask, render_template
from controllers.audio_controller import AudioController
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)

# Inicializar el controlador
audio_controller = AudioController()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    return audio_controller.handle_prediction()

if __name__ == '__main__':
    app.run(debug=True)