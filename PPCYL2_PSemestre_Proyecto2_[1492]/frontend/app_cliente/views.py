import os
import requests
import plotly.graph_objects as go
from io import BytesIO

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from .forms import LoginForm
from .decorators import rol_requerido


def login_view(request):
    if request.user.is_authenticated:
        try:
            rol = request.user.userprofile.rol

            if rol == "admin":
                return redirect("admin_dashboard")
            elif rol == "tutor":
                return redirect("tutor_dashboard")
            elif rol == "estudiante":
                return redirect("ver_notas")
        except Exception:
            logout(request)

    mensaje_error = None

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            usuario = authenticate(request, username=username, password=password)

            if usuario is not None:
                login(request, usuario)

                try:
                    rol = usuario.userprofile.rol

                    if rol == "admin":
                        return redirect("admin_dashboard")
                    elif rol == "tutor":
                        return redirect("tutor_dashboard")
                    elif rol == "estudiante":
                        return redirect("ver_notas")
                    else:
                        mensaje_error = "El usuario no tiene un rol válido."
                except Exception:
                    mensaje_error = "El usuario no tiene perfil asignado."
            else:
                mensaje_error = "Usuario o contraseña incorrectos."
    else:
        form = LoginForm()

    return render(request, "login.html", {
        "form": form,
        "error": mensaje_error
    })


def logout_view(request):
    logout(request)
    return redirect("login")

@rol_requerido("admin")
def admin_dashboard(request):
    mensaje_subida = ""
    ruta_guardada = ""

    if request.method == "POST" and request.FILES.get("archivo_xml"):
        archivo = request.FILES["archivo_xml"]

        if archivo.name.endswith(".xml"):
            ruta_destino = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "..",
                    "backend",
                    "archivos_datos",
                    "entrada",
                    "configuracion.xml"
                )
            )

            os.makedirs(os.path.dirname(ruta_destino), exist_ok=True)

            with open(ruta_destino, "wb+") as destino:
                for chunk in archivo.chunks():
                    destino.write(chunk)

            mensaje_subida = "Archivo XML cargado correctamente."
            ruta_guardada = ruta_destino
        else:
            mensaje_subida = "El archivo debe tener extensión .xml."

    url_api = "http://127.0.0.1:5000/api/configuracion"

    try:
        respuesta = requests.get(url_api)
        datos_api = respuesta.json()

        contexto = {
            "estado": datos_api.get("estado"),
            "mensaje": datos_api.get("mensaje"),
            "resumen": datos_api.get("resumen", {}),
            "validacion_salida": datos_api.get("validacion_salida", {}),
            "cursos": datos_api.get("datos", {}).get("cursos", []),
            "tutores": datos_api.get("datos", {}).get("tutores", []),
            "estudiantes": datos_api.get("datos", {}).get("estudiantes", []),
            "asignaciones_tutor": datos_api.get("datos", {}).get("asignaciones_tutor", []),
            "asignaciones_estudiante": datos_api.get("datos", {}).get("asignaciones_estudiante", []),
            "mensaje_subida": mensaje_subida,
            "ruta_guardada": ruta_guardada
        }

    except Exception as e:
        contexto = {
            "estado": "error",
            "mensaje": f"No se pudo conectar con Flask: {str(e)}",
            "resumen": {},
            "validacion_salida": {},
            "cursos": [],
            "tutores": [],
            "estudiantes": [],
            "asignaciones_tutor": [],
            "asignaciones_estudiante": [],
            "mensaje_subida": mensaje_subida,
            "ruta_guardada": ruta_guardada
        }

    return render(request, "admin_dashboard.html", contexto)

@rol_requerido("tutor")
def tutor_dashboard(request):
    mensaje_subida = ""

    if request.method == "POST":
        archivo_horarios = request.FILES.get("archivo_horarios")
        archivo_notas = request.FILES.get("archivo_notas")

        ruta_destino = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "backend",
                "archivos_datos",
                "entrada"
            )
        )

        os.makedirs(ruta_destino, exist_ok=True)

        if archivo_horarios:
            if archivo_horarios.name.endswith(".xml"):
                ruta_horarios = os.path.join(ruta_destino, "horarios.xml")
                with open(ruta_horarios, "wb+") as destino:
                    for chunk in archivo_horarios.chunks():
                        destino.write(chunk)
                mensaje_subida += "Horarios XML cargado correctamente. "
            else:
                mensaje_subida += "El archivo de horarios debe ser .xml. "

        if archivo_notas:
            if archivo_notas.name.endswith(".xml"):
                ruta_notas = os.path.join(ruta_destino, "notas.xml")
                with open(ruta_notas, "wb+") as destino:
                    for chunk in archivo_notas.chunks():
                        destino.write(chunk)
                mensaje_subida += "Notas XML cargado correctamente."
            else:
                mensaje_subida += "El archivo de notas debe ser .xml."

    url_horarios = "http://127.0.0.1:5000/api/horarios"
    url_notas = "http://127.0.0.1:5000/api/notas"
    url_reporte = "http://127.0.0.1:5000/api/reporte-matriz"
    url_resumen = "http://127.0.0.1:5000/api/notas-resumen"

    contexto = {
        "mensaje_subida": mensaje_subida,
        "estado_horarios": "error",
        "mensaje_horarios": "No cargado",
        "total_horarios": 0,
        "horarios": [],
        "estado_notas": "error",
        "mensaje_notas": "No cargado",
        "notas": [],
        "estado_reporte": "error",
        "mensaje_reporte": "No cargado",
        "url_imagen": "",
        "grafica_promedios": ""
    }

    try:
        respuesta_horarios = requests.get(url_horarios)
        datos_horarios = respuesta_horarios.json()

        contexto["estado_horarios"] = datos_horarios.get("estado")
        contexto["mensaje_horarios"] = datos_horarios.get("mensaje")
        contexto["total_horarios"] = datos_horarios.get("total", 0)
        contexto["horarios"] = datos_horarios.get("datos", [])
    except Exception as e:
        contexto["mensaje_horarios"] = f"No se pudo conectar con Flask para horarios: {str(e)}"

    try:
        respuesta_notas = requests.get(url_notas)
        datos_notas = respuesta_notas.json()

        contexto["estado_notas"] = datos_notas.get("estado")
        contexto["mensaje_notas"] = datos_notas.get("mensaje")
        contexto["notas"] = datos_notas.get("datos", [])
    except Exception as e:
        contexto["mensaje_notas"] = f"No se pudo conectar con Flask para notas: {str(e)}"

    try:
        respuesta_reporte = requests.get(url_reporte)
        datos_reporte = respuesta_reporte.json()

        contexto["estado_reporte"] = datos_reporte.get("estado")
        contexto["mensaje_reporte"] = datos_reporte.get("mensaje")
        contexto["url_imagen"] = datos_reporte.get("url_imagen", "")
    except Exception as e:
        contexto["mensaje_reporte"] = f"No se pudo conectar con Flask para Graphviz: {str(e)}"

    try:
        respuesta_resumen = requests.get(url_resumen)
        datos_resumen = respuesta_resumen.json()

        actividades = []
        promedios = []

        for item in datos_resumen.get("datos", []):
            actividades.append(item["actividad"])
            promedios.append(item["promedio"])

        figura = go.Figure(
            data=[
                go.Bar(
                    x=actividades,
                    y=promedios
                )
            ]
        )

        figura.update_layout(
            title="Promedio de notas por actividad",
            xaxis_title="Actividad",
            yaxis_title="Promedio"
        )

        contexto["grafica_promedios"] = figura.to_html(full_html=False)
    except Exception as e:
        contexto["grafica_promedios"] = f"<p>Error al generar gráfica: {str(e)}</p>"

    return render(request, "tutor_dashboard.html", contexto)

@rol_requerido("tutor")
def reporte_pdf_tutor(request):
    url_horarios = "http://127.0.0.1:5000/api/horarios"
    url_notas = "http://127.0.0.1:5000/api/notas"
    url_reporte = "http://127.0.0.1:5000/api/reporte-matriz"
    url_imagen_graphviz = "http://127.0.0.1:5000/reportes/matriz_dispersa.png"

    horarios = []
    notas = []

    try:
        respuesta_horarios = requests.get(url_horarios)
        datos_horarios = respuesta_horarios.json()
        horarios = datos_horarios.get("datos", [])
    except Exception:
        horarios = []

    try:
        respuesta_notas = requests.get(url_notas)
        datos_notas = respuesta_notas.json()
        notas = datos_notas.get("datos", [])
    except Exception:
        notas = []

    try:
        requests.get(url_reporte)
    except Exception:
        pass

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="reporte_tutor.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    y = height - 40

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(40, y, "Reporte del Tutor - PPCYL2-AcadNet")
    y -= 30

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, y, "Horarios cargados")
    y -= 20

    pdf.setFont("Helvetica", 10)
    if horarios:
        for horario in horarios:
            linea = (
                f"Curso: {horario['curso']} | Tutor: {horario['tutor']} | "
                f"Inicio: {horario['hora_inicio']} | Fin: {horario['hora_fin']}"
            )
            pdf.drawString(40, y, linea[:110])
            y -= 15

            if y < 80:
                pdf.showPage()
                y = height - 40
                pdf.setFont("Helvetica", 10)
    else:
        pdf.drawString(40, y, "No hay horarios para mostrar.")
        y -= 20

    y -= 10
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, y, "Notas cargadas")
    y -= 20

    pdf.setFont("Helvetica", 10)
    if notas:
        for nota in notas:
            linea = (
                f"Actividad: {nota['fila']} | Carnet: {nota['columna']} | Nota: {nota['valor']}"
            )
            pdf.drawString(40, y, linea[:110])
            y -= 15

            if y < 80:
                pdf.showPage()
                y = height - 40
                pdf.setFont("Helvetica", 10)
    else:
        pdf.drawString(40, y, "No hay notas para mostrar.")
        y -= 20

    pdf.showPage()
    y = height - 40

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, y, "Reporte Graphviz de la matriz dispersa")
    y -= 30

    try:
        respuesta_imagen = requests.get(url_imagen_graphviz)
        if respuesta_imagen.status_code == 200:
            imagen_bytes = BytesIO(respuesta_imagen.content)
            imagen = ImageReader(imagen_bytes)
            pdf.drawImage(
                imagen,
                40,
                300,
                width=500,
                height=180,
                preserveAspectRatio=True,
                mask='auto'
            )
        else:
            pdf.setFont("Helvetica", 10)
            pdf.drawString(40, y, "No se pudo descargar la imagen Graphviz.")
    except Exception as e:
        pdf.setFont("Helvetica", 10)
        pdf.drawString(40, y, f"Error al cargar imagen Graphviz: {str(e)}")

    pdf.save()
    return response


@rol_requerido("estudiante")
def ver_notas(request):
    url_api = "http://127.0.0.1:5000/api/notas"

    try:
        respuesta = requests.get(url_api)
        datos_api = respuesta.json()

        contexto = {
            "estado": datos_api.get("estado"),
            "mensaje": datos_api.get("mensaje"),
            "notas": datos_api.get("datos", [])
        }
    except Exception as e:
        contexto = {
            "estado": "error",
            "mensaje": f"No se pudo conectar con Flask: {str(e)}",
            "notas": []
        }

    return render(request, "estudiante_dashboard.html", contexto)