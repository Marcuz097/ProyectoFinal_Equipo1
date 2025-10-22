from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm

def registro(request):
    if request.method == 'POST':
       form = RegistroForm(request.POST)
       if form.is_valid():
         usuario = form.save() # ahora el formulario ya guarda first_name/last_name
         login(request, usuario)
         # redirige según rol
         if usuario.rol == 'admin':
            return redirect('admin_dashboard')
         elif usuario.rol == 'medico':
            return redirect('medico_dashboard')
         else:
            return redirect('paciente_dashboard')
    else:
       form = RegistroForm()
    return render(request, 'core/registro.html', {'form': form})


@login_required
def home_page(request):
    # Redirige según rol
    usuario = request.user
    if usuario.rol == 'admin':
        return redirect('admin_dashboard')
    elif usuario.rol == 'medico':
        return redirect('medico_dashboard')
    else:
        return redirect('paciente_dashboard')


@login_required
def admin_dashboard(request):
    return render(request, 'base.html')


@login_required
def medico_dashboard(request):
    return render(request, 'base.html')


@login_required
def paciente_dashboard(request):
    return render(request, 'base.html')