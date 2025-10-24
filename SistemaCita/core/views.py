from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm
from gestion_citas.forms import MedicoPerfilForm, PacientePerfilForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from gestion_citas.models import Medico, Paciente
from gestion_citas.forms import CitaForm
from gestion_citas.models import Cita
from .forms import PacienteCitaForm
from collections import defaultdict
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.utils import timezone

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
        return redirect('agenda_medico')
    else:
        return redirect('paciente_cita_list')


@login_required
def admin_dashboard(request):
    return render(request, 'base.html')


@login_required
def agenda_medico(request):
    return render(request, 'medico/agenda_medico.html')


@login_required
def paciente_cita_list(request):
    return render(request, 'paciente/paciente_cita_list.html')

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
    
# Vistas para gestión de citas por parte del paciente
# Lista de citas del paciente
class PacienteCitaListView(LoginRequiredMixin, ListView):
    model = Cita
    template_name = 'paciente/paciente_cita_list.html'
    context_object_name = 'citas'

    def get_queryset(self):
        # Solo mostrar las citas del paciente logueado
        user = self.request.user
        if user.rol == 'paciente':
            return Cita.objects.filter(paciente__usuario=user).order_by('-fecha_hora')
        return Cita.objects.none()

# Crear nueva cita
class PacienteCitaCreateView(LoginRequiredMixin, CreateView):
    model = Cita
    form_class = PacienteCitaForm
    template_name = 'paciente/paciente_cita_form.html'
    success_url = reverse_lazy('paciente_cita_list')

    def form_valid(self, form):
        # Asociar la cita al paciente logueado
        form.instance.paciente = self.request.user.paciente
        return super().form_valid(form)

class PacienteCitaUpdateView(LoginRequiredMixin, UpdateView):
    model = Cita
    form_class = PacienteCitaForm
    template_name = 'paciente/paciente_cita_form.html'
    success_url = reverse_lazy('paciente_cita_list')

    def get_queryset(self):
        # Solo puede editar sus propias citas
        return Cita.objects.filter(paciente__usuario=self.request.user)

# Eliminar cita
class PacienteCitaDeleteView(LoginRequiredMixin, DeleteView):
    model = Cita
    template_name = 'paciente/paciente_cita_delete.html'
    success_url = reverse_lazy('paciente_cita_list')

    def get_queryset(self):
        # Solo puede eliminar sus propias citas
        return Cita.objects.filter(paciente__usuario=self.request.user)
    


@login_required
def agenda_medico(request):
    # Asegurarse de que el usuario sea un medico
    try:
        medico = Medico.objects.get(usuario=request.user)
    except Medico.DoesNotExist:
        return HttpResponseForbidden("No tienes permisos de médico para ver esta página.")

    # Obtener citas del medico ordenadas
    citas = Cita.objects.filter(medico=medico).order_by('fecha_hora')

    # Agrupar por fecha (YYYY-MM-DD)
    dias = defaultdict(list)
    for c in citas:
        if c.fecha_hora:
            dia = c.fecha_hora.date()
        else:
            dia = None
        dias[dia].append(c)

    # Ordenar las claves por fecha (mostramos próximos días primero)
    dias_ordenados = sorted(dias.items(), key=lambda x: (x[0] is None, x[0]))  # None al final

    context = {
        'medico': medico,
        'dias_ordenados': dias_ordenados,
        'now': timezone.now(),
    }
    return render(request, 'medico/agenda_medico.html', context)


# Endpoint simple para actualizar estado vía AJAX (POST)
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
    # Seguridad: solo el médico dueño puede cambiar su cita
    if cita.medico != medico:
        return JsonResponse({'error': 'No autorizado a modificar esta cita'}, status=403)

    cita.estado = nuevo_estado
    cita.save()
    return JsonResponse({
        'ok': True,
        'cita_id': cita_id,
        'nuevo_estado': nuevo_estado,
    })