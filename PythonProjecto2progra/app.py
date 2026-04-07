
from flask import Flask, render_template, request, redirect, url_for, session
from users import users
import os
app = Flask(__name__)
app.secret_key = "clave_secreta"

# =========================
# LOGIN
# =========================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        for user in users:
            if user["username"] == username and user["password"] == password:
                session["user"] = username
                session["role"] = user["role"]
                return redirect(url_for("home"))

        return "Credenciales incorrectas"

    return render_template("login.html")


# =========================
# HOME
# =========================
@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("home.html", role=session["role"])


# =========================
# ADMIN (SUBIR XML)
# =========================
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if "user" not in session or session["role"] != "admin":
        return "Acceso denegado"

    if request.method == "POST":
        file = request.files["file"]

        if file and file.filename.endswith(".xml"):
            os.makedirs("data", exist_ok=True)
            file.save(os.path.join("data", file.filename))
            return "Archivo subido correctamente"
        else:
            return "Solo archivos XML"

    return render_template("admin.html")


# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
@app.route("/cargar_xml", methods=["GET", "POST"])


def cargar_xml():
    if "user" not in session or session["role"] != "admin":
        return "Acceso denegado"

    contenido = ""
    salida = ""

    if request.method == "POST":

        # Cargar archivo
        file = request.files.get("file")

        if file and file.filename.endswith(".xml"):
            filepath = os.path.join("data", file.filename)
            file.save(filepath)

            with open(filepath, "r", encoding="utf-8") as f:
                contenido = f.read()

        # Procesar XML
        if "procesar" in request.form:
            filepath = os.path.join("data", file.filename)

            tree = ET.parse(filepath)
            root = tree.getroot()

            usuarios = []

            for u in root.findall("usuario"):
                id_ = u.find("id").text
                nombre = u.find("nombre").text
                password = u.find("password").text

                usuarios.append({
                    "id": id_,
                    "nombre": nombre,
                    "password": password
                })

            salida = str(usuarios)

    return render_template("cargar.html", contenido=contenido, salida=salida)
@app.route("/ver_usuarios")
def ver_usuarios():
    if "user" not in session or session["role"] != "admin":
        return "Acceso denegado"

    return render_template("usuarios.html", users=users)

if __name__ == "__main__":
    app.run(debug=True)

    import xml.etree.ElementTree as ET

