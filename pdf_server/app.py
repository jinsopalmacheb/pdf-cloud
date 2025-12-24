from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)

# 📁 Carpeta donde se guardan los PDFs
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 🔹 Si la carpeta no existe, la crea automáticamente
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 🏠 Página principal
@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', files=files)

# ⬆️ Subir PDF
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['pdf']
    if file and file.filename.endswith('.pdf'):
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return redirect(url_for('index'))

# 📥 Descargar PDF
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

# 👁️ Abrir PDF en el navegador
@app.route('/view/<filename>')
def view(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# ▶️ Ejecutar servidor
if __name__ == '__main__':
    app.run(debug=True)
