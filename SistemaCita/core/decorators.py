from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def admin_required(view_func):
    """Permite solo a usuarios con rol=admin"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if getattr(request.user, 'rol', None) != 'admin':
            messages.error(request, "No tienes permiso para acceder al panel de administrador.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


def medico_required(view_func):
    """Permite solo a usuarios con rol=medico"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if getattr(request.user, 'rol', None) != 'medico':
            messages.error(request, "No tienes permiso para acceder al panel de médico.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


def paciente_required(view_func):
    """Permite solo a usuarios con rol=paciente"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if getattr(request.user, 'rol', None) != 'paciente':
            messages.error(request, "No tienes permiso para acceder al panel de paciente.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper