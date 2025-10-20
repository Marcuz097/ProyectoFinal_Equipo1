
from django.urls import path
from . import views

urlpatterns = [
    # Cambia 'views.home_page' por 'views.index'
    path('', views.home_page, name='home'), 
]