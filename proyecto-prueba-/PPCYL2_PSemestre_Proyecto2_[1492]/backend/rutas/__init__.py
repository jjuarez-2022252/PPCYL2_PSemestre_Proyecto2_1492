from flask import Blueprint, jsonify, send_from_directory
from estructuras.matriz_dispersa import MatrizDispersa
from analizador.lector_xml import LectorXML
from analizador.lector_configuracion import LectorConfiguracion
from analizador.lector_horarios import LectorHorarios
from analizador.reporte_graphviz import ReporteGraphviz
from analizador.generador_salida_configuracion import GeneradorSalidaConfiguracion

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

@main.route("/api/configuracion")
def obtener_configuracion():
    lector = LectorConfiguracion()
    generador = GeneradorSalidaConfiguracion()

    ruta_xml = "archivos_datos/entrada/configuracion.xml"
    ruta_salida = "archivos_datos/salida/configuraciones_aplicadas.xml"

    datos = lector.leer_configuracion(ruta_xml)
    resumen_validacion = generador.validar_y_generar_salida(datos, ruta_salida)

    resumen = {
        "total_cursos": len(datos["cursos"]),
        "total_tutores": len(datos["tutores"]),
        "total_estudiantes": len(datos["estudiantes"]),
        "total_asignaciones_tutor": len(datos["asignaciones_tutor"]),
        "total_asignaciones_estudiante": len(datos["asignaciones_estudiante"])
    }

    return jsonify({
        "estado": "ok",
        "mensaje": "Configuración cargada correctamente desde XML",
        "resumen": resumen,
        "validacion_salida": resumen_validacion,
        "datos": datos
    })


@main.route("/api/horarios")
def obtener_horarios():
    lector = LectorHorarios()
    ruta_xml = "archivos_datos/entrada/horarios.xml"

    horarios = lector.leer_horarios(ruta_xml)

    return jsonify({
        "estado": "ok",
        "mensaje": "Horarios cargados correctamente desde XML",
        "total": len(horarios),
        "datos": horarios
    })


@main.route("/api/reporte-matriz")
def obtener_reporte_matriz():
    lector = LectorXML()
    matriz = MatrizDispersa()
    reporte = ReporteGraphviz()

    ruta_xml = "archivos_datos/entrada/notas.xml"
    notas = lector.leer_notas(ruta_xml)

    for nota in notas:
        matriz.insertar(
            fila=nota["actividad"],
            columna=nota["carnet"],
            valor=nota["valor"]
        )

    reporte.generar_reporte_matriz(matriz, "matriz_dispersa")

    return jsonify({
        "estado": "ok",
        "mensaje": "Reporte Graphviz generado correctamente",
        "nombre_archivo": "matriz_dispersa.png",
        "url_imagen": "http://127.0.0.1:5000/reportes/matriz_dispersa.png"
    })

@main.route("/api/notas-resumen")
def obtener_resumen_notas():
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

    datos = matriz.recorrer_filas()

    resumen = {}

    for dato in datos:
        actividad = dato["fila"]
        valor = float(dato["valor"])

        if actividad not in resumen:
            resumen[actividad] = {
                "suma": 0,
                "cantidad": 0
            }

        resumen[actividad]["suma"] += valor
        resumen[actividad]["cantidad"] += 1

    promedios = []

    for actividad, info in resumen.items():
        promedio = info["suma"] / info["cantidad"]
        promedios.append({
            "actividad": actividad,
            "promedio": round(promedio, 2)
        })

    return jsonify({
        "estado": "ok",
        "mensaje": "Resumen de notas generado correctamente",
        "datos": promedios
    })

@main.route("/reportes/<nombre_archivo>")
def servir_reporte(nombre_archivo):
    return send_from_directory("archivos_datos/salida", nombre_archivo)