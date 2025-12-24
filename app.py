from flask import Flask, render_template, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configuración
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB

# Crear carpeta si no existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Función para validar extensión
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Página principal
@app.route("/")
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template("index.html", files=files)


# Subir PDF
@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return redirect("/")

    file = request.files["file"]

    if file.filename == "":
        return redirect("/")

    if not allowed_file(file.filename):
        return redirect("/")

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    return redirect("/")


# Ver PDF (FUNCIONA EN CELULAR)
@app.route("/view/<filename>")
def view_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename,
        as_attachment=False
    )


# Descargar PDF
@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename,
        as_attachment=True
    )


# Eliminar PDF
@app.route("/delete/<filename>")
def delete_file(filename):
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if os.path.exists(path):
        os.remove(path)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
