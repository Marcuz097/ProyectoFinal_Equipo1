# archivo de enrutamiento de la aplicación productos
from django.urls import path
# importando las vistas
from .views import (
    EspecialidadListView,
    EspecialidadCreateView,
    EspecialidadUpdateView,
    EspecialidadDeleteView,
    PacienteListView,
    PacienteCreateView,
    PacienteUpdateView,
    PacienteDeleteView,


)

# agregar un identificador de enrutamiento
app_name = "gestion_citas"

# enrutamiento
urlpatterns = [
    path('especialidades/', EspecialidadListView.as_view(), name="especialidad-list"),
    path('especialidades/nueva', EspecialidadCreateView.as_view(), name="especialidad-create"),
    path('editar/<int:pk>/', EspecialidadUpdateView.as_view(), name='especialidad-update'),
    path('eliminar/<int:pk>/', EspecialidadDeleteView.as_view(), name='especialidad-delete'),
    #pacientes
    path('pacientes/', PacienteListView.as_view(), name="paciente-list"),
    path('pacientes/nueva', PacienteCreateView.as_view(), name="paciente-create"),
    path('pacientes/editar/<int:pk>/', PacienteUpdateView.as_view(), name='paciente-update'),
    path('pacientes/eliminar/<int:pk>/', PacienteDeleteView.as_view(), name='paciente-delete'),
    #path('proveedores/', ProveedorListView.as_view(), name="proveedor-list"),
    #path('proveedores/nueva', ProveedorCreateView.as_view(), name="proveedor-create"),
    #Productos
    # Rutas de Producto
    #path('', ProductoListView.as_view(), name='producto-list'),
    #path('nuevo/', ProductoCreateView.as_view(), name='producto-create'),
    
    # Rutas BONUS
   # path('editar/<int:pk>/', ProductoUpdateView.as_view(), name='producto-update'),
    #path('eliminar/<int:pk>/', ProductoDeleteView.as_view(), name='producto-delete'),
]
