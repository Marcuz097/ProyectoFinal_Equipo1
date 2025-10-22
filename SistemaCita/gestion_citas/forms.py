from django import forms
from .models import Paciente 
from .models import Medico
from .models import Cita
from .models import Especialidad
from django.contrib.auth import get_user_model

User = get_user_model()



# Formulario para Paciente
class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['usuario', 'fecha_nacimiento', 'telefono', 'direccion']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'usuario': forms.Select(attrs={'class': 'form-select'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 🔹 Solo mostrar usuarios con rol = 'paciente'
        self.fields['usuario'].queryset = User.objects.filter(rol='paciente')
        self.fields['usuario'].label_from_instance = lambda obj: f"{obj.username} ({obj.first_name} {obj.last_name})"

# Formulario para Medico
class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['usuario', 'matricula', 'telefono', 'especialidades']
        widgets = {
            'matricula': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidades': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'usuario': forms.Select(attrs={'class': 'form-select'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 🔹 Solo mostrar usuarios con rol = 'medico'
        self.fields['usuario'].queryset = User.objects.filter(rol='medico')
        # 🔹 Mostrar nombre completo en el combo
        self.fields['usuario'].label_from_instance = lambda obj: f"{obj.username} ({obj.first_name} {obj.last_name})"

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 🔹 Solo mostrar pacientes válidos (con rol paciente)
        self.fields['paciente'].queryset = Paciente.objects.select_related('usuario').all()
        self.fields['paciente'].label_from_instance = lambda obj: f"{obj.usuario.first_name} {obj.usuario.last_name}"

        # 🔹 Solo mostrar médicos válidos (con rol medico)
        self.fields['medico'].queryset = Medico.objects.select_related('usuario').all()
        self.fields['medico'].label_from_instance = lambda obj: f"Dr(a). {obj.usuario.first_name} {obj.usuario.last_name}"

# Formulario para Especialidad
class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }

