import os
from flask import Flask, request, render_template_string, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_DIR = "/var/www/mon-app/uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
# Limite la taille des uploads à 16 Mo pour des raisons de sécurité
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# S'assurer que le dossier d'upload existe
os.makedirs(UPLOAD_DIR, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Template HTML intégré (Style moderne et responsive)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Galerie Photo Flask</title>
    <style>
        body { font-family: system-ui, sans-serif; background: #f4f6f9; color: #333; margin: 0; padding: 20px; }
        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        h1, h2 { color: #2c3e50; }
        .upload-form { background: #ebf3f9; padding: 20px; border-radius: 6px; border: 1px solid #cedbe5; margin-bottom: 30px; }
        .gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 20px; margin-top: 20px; }
        .gallery-item { border: 1px solid #ddd; background: #fff; border-radius: 6px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.05); text-align: center; }
        .gallery-item img { width: 100%; height: 150px; object-fit: cover; display: block; border-bottom: 1px solid #ddd; transition: transform 0.2s; }
        .gallery-item img:hover { transform: scale(1.05); }
        .filename { font-size: 0.85rem; padding: 8px; text-overflow: ellipsis; overflow: hidden; white-space: nowrap; color: #555; }
        .alert { padding: 12px; margin-bottom: 15px; border-radius: 4px; font-weight: bold; }
        .success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        input[type="file"] { margin-right: 10px; }
        input[type="submit"] { background: #3498db; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; }
        input[type="submit"]:hover { background: #2980b9; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📷 Galerie Photo Flask</h1>

        {% if msg_success %}
            <div class="alert success">{{ msg_success }}</div>
        {% endif %}
        {% if msg_error %}
            <div class="alert error">{{ msg_error }}</div>
        {% endif %}

        <div class="upload-form">
            <h2>Téléverser une image</h2>
            <form method="POST" enctype="multipart/form-data" action="/">
                <input type="file" name="image_file" accept="image/*" required>
                <input type="submit" value="Envoyer la photo">
            </form>
        </div>

        <h2>Navigation des Photos</h2>
        <div class="gallery">
            {% for img in images %}
                <div class="gallery-item">
                    <a href="{{ url_for('uploaded_file', filename=img) }}" target="_blank">
                        <img src="{{ url_for('uploaded_file', filename=img) }}" alt="{{ img }}">
                    </a>
                    <div class="filename" title="{{ img }}">{{ img }}</div>
                </div>
            {% else %}
                <p>Aucune photo pour le moment.</p>
            {% endfor %}
        </div>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    msg_success = None
    msg_error = None

    if request.method == 'POST':
        if 'image_file' not in request.files:
            msg_error = "Aucun fichier détecté."
        else:
            file = request.files['image_file']
            if file.filename == '':
                msg_error = "Aucun fichier sélectionné."
            elif file and allowed_file(file.filename):
                # secure_filename nettoie le nom (ex: supprime les espaces ou les '../' malveillants)
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_DIR, filename))
                msg_success = f"Image '{filename}' ajoutée avec succès !"
            else:
                msg_error = "Extension non autorisée (Uniquement JPG, PNG, GIF, WEBP)."

    # Lister et trier les images existantes
    images = [f for f in os.listdir(UPLOAD_DIR) if allowed_file(f)]
    images.sort()

    return render_template_string(HTML_TEMPLATE, images=images, msg_success=msg_success, msg_error=msg_error)

# Route pour servir de manière sécurisée les fichiers stockés
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)

# Requis pour l'exécution directe en local pour le dev (python app.py)
if __name__ == '__main__':
    app.run(debug=True)

