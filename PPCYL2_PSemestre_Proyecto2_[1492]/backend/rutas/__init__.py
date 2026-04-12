from flask import Blueprint, jsonify
from estructuras.matriz_dispersa import MatrizDispersa
from analizador.lector_xml import LectorXML

main = Blueprint("main", __name__)

@main.route("/")
def inicio():
    return jsonify({
        "mensaje": "Backend Flask de PPCYL2-AcadNet funcionando correctamente"
    })

@main.route("/api/test")
def prueba_api():
    return jsonify({
        "estado": "ok",
        "proyecto": "PPCYL2-AcadNet",
        "modulo": "Backend Flask"
    })

@main.route("/api/notas")
def obtener_notas():
    lector = LectorXML()
    matriz = MatrizDispersa()

    ruta_xml = "archivos_datos/entrada/notas.xml"
    notas = lector.leer_notas(ruta_xml)

    for nota in notas:
        matriz.insertar(
            fila=nota["actividad"],
            columna=nota["carnet"],
            valor=nota["valor"]
        )

    return jsonify({
        "estado": "ok",
        "mensaje": "Notas cargadas correctamente desde XML",
        "datos": matriz.recorrer_filas()
    })