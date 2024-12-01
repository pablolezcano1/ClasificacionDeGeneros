# run.py
from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Asegurarnos de que existe el directorio de uploads
    os.makedirs(os.path.join('app', 'static', 'uploads'), exist_ok=True)
    app.run(threaded=False)  # Desactiva el uso de subprocesos
    app.run(debug=True)