from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test


def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.rol in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect("Sin_Acceso")

        return wrapper

    return decorator
