from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, CustomLogoutView


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('registro/', views.registro, name='registro'),

    path('', views.home_page, name='home'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    path('paciente/citas/', views.PacienteCitaListView.as_view(), name='paciente_cita_list'),
    path('paciente/citas/nueva/', views.PacienteCitaCreateView.as_view(), name='paciente_cita_create'),
    path('paciente/citas/<int:pk>/editar/', views.PacienteCitaUpdateView.as_view(), name='paciente_cita_edit'),
    path('paciente/citas/<int:pk>/eliminar/', views.PacienteCitaDeleteView.as_view(), name='paciente_cita_delete'),
    
   
    path('completar-perfil/paciente/', views.completar_perfil_paciente, name='completar_perfil_paciente'),
    
    path('medico/agenda/', views.agenda_medico, name='agenda_medico'),
    path('medico/actualizar-estado/', views.actualizar_estado_cita, name='medico-actualizar-estado'),
]