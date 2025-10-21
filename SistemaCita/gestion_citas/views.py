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