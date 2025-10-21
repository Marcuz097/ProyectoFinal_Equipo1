from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = [
        ('admin', 'Administrador'),
        ('medico', 'Médico'),
        ('paciente', 'Paciente'),
    ]
    rol = models.CharField(max_length=20, choices=ROLES, default='paciente')

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"