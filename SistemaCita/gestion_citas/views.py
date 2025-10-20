from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Especialidad

# Create your views here.
#importar reverse_lazy de urls para redireccionar la respuesta de un formulario
from django.urls import reverse_lazy

# crear vistas genericas para categoria
class EspecialidadListView(ListView):

    # indicar cual es el modelo base
    model = Especialidad
    fields = ["nombre", ]
    template_name = "especialidades/especialidad-list.html"
    context_object_name = "especialidades"
