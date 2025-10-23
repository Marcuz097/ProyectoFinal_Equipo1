from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm
from gestion_citas.forms import MedicoPerfilForm, PacientePerfilForm
from gestion_citas.models import Medico, Paciente

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
            return redirect('completar_perfil_medico')
         elif usuario.rol == 'paciente':
            return redirect('completar_perfil_paciente')
         else:
            return redirect('base')
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

# Vista para médicos
def completar_perfil_medico(request):
 user = request.user
 form = MedicoPerfilForm(request.POST or None)
 
 
 if request.method == 'POST' and form.is_valid():
        medico = form.save(commit=False)
        medico.usuario = user
        medico.save()
        form.save_m2m()
        return redirect('home')

    # En GET, el formulario se renderiza vacío correctamente
 return render(request, 'core/completar_perfil.html', {
        'form': form,
        'tipo': 'Médico'
 })

# Vista para pacientes
def completar_perfil_paciente(request):
    user = request.user
    form = PacientePerfilForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        paciente = form.save(commit=False)
        paciente.usuario = user
        paciente.save()
        return redirect('home')

    return render(request, 'core/completar_perfil.html', {
        'form': form,
        'tipo': 'Paciente'
    })