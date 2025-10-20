# archivo de enrutamiento de la aplicación productos
from django.urls import path
# importando las vistas
from .views import (
    EspecialidadListView,
    EspecialidadCreateView


)

# agregar un identificador de enrutamiento
app_name = "gestion_citas"

# enrutamiento
urlpatterns = [
    path('especialidades/', EspecialidadListView.as_view(), name="especialidad-list"),
    path('especialidades/nueva', EspecialidadCreateView.as_view(), name="especialidad-create"),
    #proveedores
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
