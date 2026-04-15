from flask import Flask
from flask_cors import CORS
from rutas import main

app = Flask(__name__)
CORS(app)

app.config["SECRET_KEY"] = "clave_basica_proyecto"

app.register_blueprint(main)

if __name__ == "__main__":
    app.run(debug=True)