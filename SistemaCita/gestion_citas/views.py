from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Paciente, Medico, Cita, Especialidad
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy

from .forms import PacienteForm
from .forms import MedicoForm
from .forms import CitaForm
from .forms import EspecialidadForm

# Especialidad
class EspecialidadListView(LoginRequiredMixin, ListView):
    model = Especialidad
    template_name = 'especialidad/especialidad-list.html'
    context_object_name = 'especialidades'

class EspecialidadCreateView(CreateView):
    model = Especialidad
    form_class = EspecialidadForm
    template_name = 'especialidad/especialidad-form.html'
    success_url = reverse_lazy('gestion_citas:especialidad-list')


class EspecialidadUpdateView(UpdateView):
    model = Especialidad
    fields = ['nombre']
    template_name = "especialidad/especialidad-form.html"
    success_url = reverse_lazy('gestion_citas:especialidad-list')

class EspecialidadDeleteView(DeleteView):
    model = Especialidad
    template_name = "especialidad/especialidad-delete.html" # Plantilla para confirmar eliminación
    success_url = reverse_lazy('gestion_citas:especialidad-list') 

class PacienteListView(LoginRequiredMixin, ListView):
    model = Paciente
    template_name = 'paciente/paciente-list.html'
    context_object_name = 'pacientes'
    def get_queryset(self):
        # Solo usuarios con rol "paciente"
        return Paciente.objects.filter(usuario__rol='paciente')

class PacienteCreateView(CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'paciente/paciente-form.html'
    success_url = reverse_lazy('gestion_citas:paciente-list')

class PacienteUpdateView(UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'paciente/paciente-form.html'
    success_url = reverse_lazy('gestion_citas:paciente-list')

class PacienteDeleteView(DeleteView):
    model = Paciente
    template_name = 'paciente/paciente-delete.html'
    success_url = reverse_lazy('gestion_citas:paciente-list')

class MedicoListView(LoginRequiredMixin, ListView):
    model = Medico
    template_name = 'medico/medico-list.html'
    context_object_name = 'medicos'
    def get_queryset(self):
        # Solo usuarios con rol "medico"
        return Medico.objects.filter(usuario__rol='medico')

class MedicoCreateView(CreateView):
    model = Medico
    form_class = MedicoForm
    template_name = 'medico/medico-form.html'
    success_url = reverse_lazy('gestion_citas:medico-list')

class MedicoUpdateView(UpdateView):
    model = Medico
    form_class = MedicoForm
    template_name = 'medico/medico-form.html'
    success_url = reverse_lazy('gestion_citas:medico-list')

class MedicoDeleteView(DeleteView):
    model = Medico
    template_name = 'medico/medico-delete.html'
    success_url = reverse_lazy('gestion_citas:medico-list')

class CitaListView(LoginRequiredMixin, ListView):
    model = Cita
    template_name = 'cita/cita-list.html'
    context_object_name = 'citas'
    def get_queryset(self):
        user = self.request.user
        # Si es admin: todas las citas
        if user.rol == 'admin':
            return Cita.objects.all()
        # Si es médico: solo las citas del médico logueado
        elif user.rol == 'medico':
            return Cita.objects.filter(medico__usuario=user)
        # Si es paciente: solo sus citas
        elif user.rol == 'paciente':
            return Cita.objects.filter(paciente__usuario=user)
        else:
            return Cita.objects.none()

class CitaCreateView(CreateView):
    model = Cita
    form_class = CitaForm
    template_name = 'cita/cita-form.html'
    success_url = reverse_lazy('gestion_citas:cita-list')

class CitaUpdateView(UpdateView):
    model = Cita
    form_class = CitaForm
    template_name = 'cita/cita-form.html'
    success_url = reverse_lazy('gestion_citas:cita-list')

class CitaDeleteView(DeleteView):
    model = Cita
    template_name = 'cita/cita-delete.html'
    success_url = reverse_lazy('gestion_citas:cita-list')

