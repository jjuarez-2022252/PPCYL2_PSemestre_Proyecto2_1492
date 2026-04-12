import requests
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
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
    return render(request, "admin_dashboard.html")


@rol_requerido("tutor")
def tutor_dashboard(request):
    return render(request, "tutor_dashboard.html")


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