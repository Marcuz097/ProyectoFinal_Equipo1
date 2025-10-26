from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.http import JsonResponse, HttpResponseForbidden
from collections import defaultdict

from .forms import RegistroForm, PacienteCitaForm
from gestion_citas.forms import PacientePerfilForm
from django.contrib import messages
from .forms import MedicoRegistroForm
from gestion_citas.models import Medico, Paciente, Cita
from .decorators import admin_required, medico_required, paciente_required
from .mixins import RolRequiredMixin


# ==========================================================
# 🔹 Login y Logout personalizados
# ==========================================================
class CustomLoginView(LoginView):
    template_name = "core/login.html"
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')  # Redirige al login tras cerrar sesión


# ==========================================================
# 🔹 Registro de usuario
# ==========================================================
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión automáticamente
            # Redirige a completar el registro de paciente
            return redirect('completar_perfil_paciente')  
    else:
        form = RegistroForm()
    return render(request, 'core/registro.html', {'form': form})


# ==========================================================
# 🔹 Vistas según rol
# ==========================================================
@login_required
def home_page(request):
    usuario = request.user
    if usuario.rol == 'admin':
        return redirect('admin_dashboard')
    elif usuario.rol == 'medico':
        return redirect('agenda_medico')
    else:
        return redirect('paciente_cita_list')

@login_required
@admin_required
def admin_dashboard(request):
    return render(request, 'base.html')


@medico_required
def agenda_medico(request):
    try:
        medico = Medico.objects.get(usuario=request.user)
    except Medico.DoesNotExist:
        return HttpResponseForbidden("No tienes permisos de médico para ver esta página.")

    citas = Cita.objects.filter(medico=medico).order_by('fecha_hora')

    dias = defaultdict(list)
    for c in citas:
        dia = c.fecha_hora.date() if c.fecha_hora else None
        dias[dia].append(c)

    dias_ordenados = sorted(dias.items(), key=lambda x: (x[0] is None, x[0]))

    context = {
        'medico': medico,
        'dias_ordenados': dias_ordenados,
        'now': timezone.now(),
    }
    return render(request, 'medico/agenda_medico.html', context)


@paciente_required
def paciente_cita_list(request):
    return render(request, 'paciente/paciente_cita_list.html')


# ==========================================================
# 🔹 Completar perfil
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


# ==========================================================
# 🔹 CRUD de citas del paciente
# ==========================================================
class PacienteCitaListView(RolRequiredMixin, ListView):
    model = Cita
    rol_permitido = 'paciente'
    template_name = 'paciente/paciente_cita_list.html'
    context_object_name = 'citas'

    def get_queryset(self):
        user = self.request.user
        if user.rol == 'paciente':
            return Cita.objects.filter(paciente__usuario=user).order_by('-fecha_hora')
        return Cita.objects.none()


class PacienteCitaCreateView(RolRequiredMixin, CreateView):
    model = Cita
    rol_permitido = 'paciente'
    form_class = PacienteCitaForm
    template_name = 'paciente/paciente_cita_form.html'
    success_url = reverse_lazy('paciente_cita_list')

    def form_valid(self, form):
        form.instance.paciente = self.request.user.paciente
        return super().form_valid(form)


class PacienteCitaUpdateView(RolRequiredMixin, UpdateView):
    model = Cita
    rol_permitido = 'paciente'
    form_class = PacienteCitaForm
    template_name = 'paciente/paciente_cita_form.html'
    success_url = reverse_lazy('paciente_cita_list')

    def get_queryset(self):
        return Cita.objects.filter(paciente__usuario=self.request.user)


class PacienteCitaDeleteView(RolRequiredMixin, DeleteView):
    model = Cita
    rol_permitido = 'paciente'
    template_name = 'paciente/paciente_cita_delete.html'
    success_url = reverse_lazy('paciente_cita_list')

    def get_queryset(self):
        return Cita.objects.filter(paciente__usuario=self.request.user)


# ==========================================================
# 🔹 AJAX: Actualizar estado de cita
# ==========================================================
@login_required
@require_POST
def actualizar_estado_cita(request):
    try:
        medico = Medico.objects.get(usuario=request.user)
    except Medico.DoesNotExist:
        return JsonResponse({'error': 'No autorizado'}, status=403)

    cita_id = request.POST.get('cita_id')
    nuevo_estado = request.POST.get('estado')
    if not cita_id or not nuevo_estado:
        return JsonResponse({'error': 'Datos incompletos'}, status=400)

    cita = get_object_or_404(Cita, pk=cita_id)
    if cita.medico != medico:
        return JsonResponse({'error': 'No autorizado a modificar esta cita'}, status=403)

    cita.estado = nuevo_estado
    cita.save()
    return JsonResponse({
        'ok': True,
        'cita_id': cita_id,
        'nuevo_estado': nuevo_estado,
    })

@login_required
@admin_required
def registrar_medico(request):
    if not request.user.rol == 'admin':
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')  # o donde quieras redirigir si no es admin

    if request.method == 'POST':
        form = MedicoRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Médico registrado correctamente.")
            return redirect('gestion_citas:medico-list')  # o vuelve al listado de médicos
    else:
        form = MedicoRegistroForm()

    return render(request, 'admin/registrar_medico.html', {'form': form})