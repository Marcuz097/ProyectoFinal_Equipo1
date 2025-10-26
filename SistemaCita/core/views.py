from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.http import JsonResponse, HttpResponseForbidden
from collections import defaultdict

# Formularios importados
from .forms import RegistroForm, PacienteCitaForm
from gestion_citas.forms import PacientePerfilForm
from django.contrib import messages
from .forms import MedicoRegistroForm

# Modelos
from gestion_citas.models import Medico, Paciente, Cita

# Decoradores de rol
from .decorators import admin_required, medico_required, paciente_required

# Mixins para vistas basadas en clases
from .mixins import RolRequiredMixin


# ==========================================================
# 🔹 LOGIN Y LOGOUT PERSONALIZADOS
# ==========================================================
class CustomLoginView(LoginView):
    template_name = "core/login.html"  # Plantilla para login
    redirect_authenticated_user = True  # Redirige si ya está logueado


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')  # Redirige al login tras cerrar sesión


# ==========================================================
# 🔹 REGISTRO DE USUARIO
# ==========================================================
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)  # Se reciben datos del formulario
        if form.is_valid():  # Validación de formulario
            user = form.save()  # Guarda el usuario
            login(request, user)  # Inicia sesión automáticamente
            # Redirige a completar perfil de paciente
            return redirect('completar_perfil_paciente')  
    else:
        form = RegistroForm()  # Formulario vacío si GET
    return render(request, 'core/registro.html', {'form': form})


# ==========================================================
# 🔹 VISTAS SEGÚN ROL
# ==========================================================
@login_required
def home_page(request):
    usuario = request.user
    # Redirige según rol del usuario
    if usuario.rol == 'admin':
        return redirect('admin_dashboard')
    elif usuario.rol == 'medico':
        return redirect('agenda_medico')
    else:
        return redirect('paciente_cita_list')


@login_required
@admin_required
def admin_dashboard(request):
    # Renderiza dashboard de admin
    return render(request, 'base.html')


@medico_required
def agenda_medico(request):
    # Obtiene el médico logueado
    try:
        medico = Medico.objects.get(usuario=request.user)
    except Medico.DoesNotExist:
        return HttpResponseForbidden("No tienes permisos de médico para ver esta página.")

    # Obtiene las citas del médico
    citas = Cita.objects.filter(medico=medico).order_by('fecha_hora')

    # Agrupa citas por día
    dias = defaultdict(list)
    for c in citas:
        dia = c.fecha_hora.date() if c.fecha_hora else None
        dias[dia].append(c)

    # Ordena los días (None al final)
    dias_ordenados = sorted(dias.items(), key=lambda x: (x[0] is None, x[0]))

    context = {
        'medico': medico,
        'dias_ordenados': dias_ordenados,
        'now': timezone.now(),
    }
    return render(request, 'medico/agenda_medico.html', context)


@paciente_required
def paciente_cita_list(request):
    # Renderiza la lista de citas del paciente
    return render(request, 'paciente/paciente_cita_list.html')


# ==========================================================
# 🔹 COMPLETAR PERFIL DE PACIENTE
# ==========================================================
def completar_perfil_paciente(request):
    user = request.user
    form = PacientePerfilForm(request.POST or None)  # Formulario con POST o vacío

    if request.method == 'POST' and form.is_valid():
        paciente = form.save(commit=False)  # No guarda todavía
        paciente.usuario = user  # Asigna usuario logueado
        paciente.save()  # Guarda paciente
        return redirect('home')

    return render(request, 'core/completar_perfil.html', {
        'form': form,
        'tipo': 'Paciente'
    })


# ==========================================================
# 🔹 CRUD DE CITAS DEL PACIENTE
# ==========================================================
class PacienteCitaListView(RolRequiredMixin, ListView):
    model = Cita
    rol_permitido = 'paciente'  # Solo pacientes
    template_name = 'paciente/paciente_cita_list.html'
    context_object_name = 'citas'

    def get_queryset(self):
        user = self.request.user
        if user.rol == 'paciente':
            # Filtra citas solo del paciente logueado
            return Cita.objects.filter(paciente__usuario=user).order_by('-fecha_hora')
        return Cita.objects.none()


class PacienteCitaCreateView(RolRequiredMixin, CreateView):
    model = Cita
    rol_permitido = 'paciente'
    form_class = PacienteCitaForm
    template_name = 'paciente/paciente_cita_form.html'
    success_url = reverse_lazy('paciente_cita_list')

    def form_valid(self, form):
        # Asigna paciente automáticamente al crear cita
        form.instance.paciente = self.request.user.paciente
        return super().form_valid(form)


class PacienteCitaUpdateView(RolRequiredMixin, UpdateView):
    model = Cita
    rol_permitido = 'paciente'
    form_class = PacienteCitaForm
    template_name = 'paciente/paciente_cita_form.html'
    success_url = reverse_lazy('paciente_cita_list')

    def get_queryset(self):
        # Solo permite actualizar citas del paciente logueado
        return Cita.objects.filter(paciente__usuario=self.request.user)


class PacienteCitaDeleteView(RolRequiredMixin, DeleteView):
    model = Cita
    rol_permitido = 'paciente'
    template_name = 'paciente/paciente_cita_delete.html'
    success_url = reverse_lazy('paciente_cita_list')

    def get_queryset(self):
        # Solo permite eliminar citas del paciente logueado
        return Cita.objects.filter(paciente__usuario=self.request.user)


# ==========================================================
# 🔹 AJAX: ACTUALIZAR ESTADO DE CITA
# ==========================================================
@login_required
@require_POST
def actualizar_estado_cita(request):
    # Verifica que sea médico
    try:
        medico = Medico.objects.get(usuario=request.user)
    except Medico.DoesNotExist:
        return JsonResponse({'error': 'No autorizado'}, status=403)

    # Obtiene datos del POST
    cita_id = request.POST.get('cita_id')
    nuevo_estado = request.POST.get('estado')
    if not cita_id or not nuevo_estado:
        return JsonResponse({'error': 'Datos incompletos'}, status=400)

    # Obtiene la cita
    cita = get_object_or_404(Cita, pk=cita_id)
    if cita.medico != medico:
        return JsonResponse({'error': 'No autorizado a modificar esta cita'}, status=403)

    # Actualiza estado y guarda
    cita.estado = nuevo_estado
    cita.save()
    return JsonResponse({
        'ok': True,
        'cita_id': cita_id,
        'nuevo_estado': nuevo_estado,
    })


# ==========================================================
# 🔹 REGISTRAR MÉDICO (ADMIN)
# ==========================================================
@login_required
@admin_required
def registrar_medico(request):
    # Verifica que sea admin
    if not request.user.rol == 'admin':
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')

    if request.method == 'POST':
        form = MedicoRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Médico registrado correctamente.")
            return redirect('gestion_citas:medico-list')  # Redirige al listado de médicos
    else:
        form = MedicoRegistroForm()

    return render(request, 'admin/registrar_medico.html', {'form': form})