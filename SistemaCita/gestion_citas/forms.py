from django import forms
from .models import Paciente 
from .models import Medico
from .models import Cita
from .models import Especialidad


# Formulario para Paciente
class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['usuario', 'fecha_nacimiento', 'telefono', 'direccion']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Formulario para Medico
class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['usuario', 'matricula', 'telefono', 'especialidades']
        widgets = {
            'matricula': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidades': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

# Formulario para Cita
class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['fecha_hora', 'motivo', 'estado', 'paciente', 'medico']
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control'}),
            'estado': forms.Select(choices=[
                ('Pendiente', 'Pendiente'),
                ('Confirmada', 'Confirmada'),
                ('Cancelada', 'Cancelada'),
                ('Completada', 'Completada')
            ], attrs={'class': 'form-select'}),
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'medico': forms.Select(attrs={'class': 'form-select'}),
        }

# Formulario para Especialidad
class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }

