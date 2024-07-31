from functools import wraps
from django.shortcuts import redirect


def require_role(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("Sin_Acceso")

            if request.user.rol != required_role:
                return redirect("Sin_Acceso")

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
