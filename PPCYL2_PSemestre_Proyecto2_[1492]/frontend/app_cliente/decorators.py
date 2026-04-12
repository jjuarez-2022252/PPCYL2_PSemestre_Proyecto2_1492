from django.shortcuts import redirect


def rol_requerido(rol_permitido):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")

            try:
                if request.user.userprofile.rol != rol_permitido:
                    return redirect("login")
            except Exception:
                return redirect("login")

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator