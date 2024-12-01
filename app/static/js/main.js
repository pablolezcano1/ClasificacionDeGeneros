// static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('uploadForm');
    const fileInput = form.querySelector('input[type="file"]');
    const preview = document.getElementById('preview');
    const loading = document.getElementById('loading');
    
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            // Verificar tamaño del archivo (50MB en bytes)
            if (file.size > 50 * 1024 * 1024) {
                alert('El archivo es demasiado grande. El tamaño máximo es 50MB.');
                fileInput.value = ''; // Limpiar el input
                return;
            }
            
            const audio = preview.querySelector('audio');
            audio.src = URL.createObjectURL(file);
            preview.classList.remove('hidden');
        }
    });
    
    form.addEventListener('submit', function(e) {
        const file = fileInput.files[0];
        if (file && file.size > 50 * 1024 * 1024) {
            e.preventDefault();
            alert('El archivo es demasiado grande. El tamaño máximo es 50MB.');
            return;
        }
        loading.classList.remove('hidden');
    });
});