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
    path('paciente/dashboard/', views.paciente_dashboard, name='paciente_dashboard'),
]