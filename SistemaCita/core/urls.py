from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro, name='registro'),

    path('', views.home_page, name='home'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('medico/dashboard/', views.medico_dashboard, name='medico_dashboard'),
    
    path('paciente/citas/', views.PacienteCitaListView.as_view(), name='paciente_cita_list'),
    path('paciente/citas/nueva/', views.PacienteCitaCreateView.as_view(), name='paciente_cita_create'),
    path('paciente/citas/<int:pk>/editar/', views.PacienteCitaUpdateView.as_view(), name='paciente_cita_edit'),
    path('paciente/citas/<int:pk>/eliminar/', views.PacienteCitaDeleteView.as_view(), name='paciente_cita_delete'),
    
    path('completar-perfil/medico/', views.completar_perfil_medico, name='completar_perfil_medico'),
    path('completar-perfil/paciente/', views.completar_perfil_paciente, name='completar_perfil_paciente'),
]