from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Paciente, Medico, Cita, Especialidad
from django.contrib import messages

from django.urls import reverse_lazy

from .forms import PacienteForm
from .forms import MedicoForm
from .forms import CitaForm
from .forms import EspecialidadForm
from core.mixins import RolRequiredMixin

# Especialidad
class EspecialidadListView(RolRequiredMixin, ListView):
    model = Especialidad
    rol_permitido = 'admin'
    template_name = 'especialidad/especialidad-list.html'
    context_object_name = 'especialidades'

class EspecialidadCreateView(RolRequiredMixin, CreateView):
    model = Especialidad
    rol_permitido = 'admin'
    form_class = EspecialidadForm
    template_name = 'especialidad/especialidad-form.html'
    success_url = reverse_lazy('gestion_citas:especialidad-list')


class EspecialidadUpdateView(RolRequiredMixin, UpdateView):
    model = Especialidad
    rol_permitido = 'admin'
    fields = ['nombre']
    template_name = "especialidad/especialidad-form.html"
    success_url = reverse_lazy('gestion_citas:especialidad-list')

class EspecialidadDeleteView(RolRequiredMixin, DeleteView):
    model = Especialidad
    rol_permitido = 'admin'
    template_name = "especialidad/especialidad-delete.html" # Plantilla para confirmar eliminación
    success_url = reverse_lazy('gestion_citas:especialidad-list') 

class PacienteListView(RolRequiredMixin, ListView):
    model = Paciente
    rol_permitido = 'admin'
    template_name = 'paciente/paciente-list.html'
    context_object_name = 'pacientes'
    def get_queryset(self):
        # Solo usuarios con rol "paciente"
        return Paciente.objects.filter(usuario__rol='paciente')

class PacienteCreateView(RolRequiredMixin, CreateView):
    model = Paciente
    rol_permitido = 'admin'
    form_class = PacienteForm
    template_name = 'paciente/paciente-form.html'
    success_url = reverse_lazy('gestion_citas:paciente-list')

class PacienteUpdateView(RolRequiredMixin, UpdateView):
    model = Paciente
    rol_permitido = 'admin'
    form_class = PacienteForm
    template_name = 'paciente/paciente-form.html'
    success_url = reverse_lazy('gestion_citas:paciente-list')

class PacienteDeleteView(RolRequiredMixin, DeleteView):
    model = Paciente
    rol_permitido = 'admin'
    template_name = 'paciente/paciente-delete.html'
    success_url = reverse_lazy('gestion_citas:paciente-list')

class MedicoListView(RolRequiredMixin, ListView):
    model = Medico
    rol_permitido = 'admin'
    template_name = 'medico/medico-list.html'
    context_object_name = 'medicos'
    def get_queryset(self):
        # Solo usuarios con rol "medico"
        return Medico.objects.filter(usuario__rol='medico')

class MedicoCreateView(RolRequiredMixin, CreateView):
    model = Medico
    rol_permitido = 'admin'
    form_class = MedicoForm
    template_name = 'medico/medico-form.html'
    success_url = reverse_lazy('gestion_citas:medico-list')

class MedicoUpdateView(RolRequiredMixin, UpdateView):
    model = Medico
    rol_permitido = 'admin'
    form_class = MedicoForm
    template_name = 'medico/medico-form.html'
    success_url = reverse_lazy('gestion_citas:medico-list')

class MedicoDeleteView(RolRequiredMixin,DeleteView):
    model = Medico
    rol_permitido = 'admin'
    template_name = 'medico/medico-delete.html'
    success_url = reverse_lazy('gestion_citas:medico-list')

class CitaListView(RolRequiredMixin, ListView):
    model = Cita
    template_name = 'cita/cita-list.html'
    context_object_name = 'citas'

    # Solo los roles permitidos pueden entrar a esta vista
    rol_permitido= 'admin'  # Puede ser 'admin', 'medico' o 'paciente'

    def get_queryset(self):
        user = self.request.user

        if user.rol == 'admin':
            # Admin ve todas las citas
            return Cita.objects.all()
        elif user.rol == 'medico':
            # Médico solo ve sus citas
            return Cita.objects.filter(medico__usuario=user)
        elif user.rol == 'paciente':
            # Paciente solo ve sus citas
            return Cita.objects.filter(paciente__usuario=user)
        else:
            # Otros roles no ven nada
            return Cita.objects.none()

class CitaCreateView(RolRequiredMixin, CreateView):
    model = Cita
    rol_permitido = 'admin'
    form_class = CitaForm
    template_name = 'cita/cita-form.html'
    success_url = reverse_lazy('gestion_citas:cita-list')

class CitaUpdateView(RolRequiredMixin,UpdateView):
    model = Cita
    rol_permitido = 'admin'
    form_class = CitaForm
    template_name = 'cita/cita-form.html'
    success_url = reverse_lazy('gestion_citas:cita-list')

class CitaDeleteView(RolRequiredMixin,DeleteView):
    model = Cita
    rol_permitido = 'admin'
    template_name = 'cita/cita-delete.html'
    success_url = reverse_lazy('gestion_citas:cita-list')
    

