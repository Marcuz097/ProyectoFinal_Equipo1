from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Paciente, Medico, Cita, Especialidad

from django.urls import reverse_lazy

from .forms import PacienteForm
from .forms import MedicoForm
from .forms import CitaForm
from .forms import EspecialidadForm

# Especialidad
class EspecialidadListView(ListView):
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