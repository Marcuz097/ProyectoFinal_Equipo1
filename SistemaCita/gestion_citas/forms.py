from django import forms
from .models import Paciente 
from .models import Medico
from .models import Cita
from .models import Especialidad 
# 
from django.contrib.auth import get_user_model
# 
from django.utils import timezone
import re
from datetime import date

# Obtener el modelo de usuario actual (puede ser personalizado)
User = get_user_model()


# ==============================
# FORMULARIO PARA PACIENTE
# ==============================
class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        # Campos que se van a mostrar en el formulario
        fields = ['usuario', 'fecha_nacimiento', 'telefono', 'direccion']
        # Widgets para personalizar la apariencia de los campos
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control',
                'max': '9999-12-31',  # fecha máxima
                'required': False
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ejemplo: 7777-7777',
                'required': False
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ejemplo: Calle 5, San Salvador',
                'required': False
            }),
            'usuario': forms.Select(attrs={'class': 'form-select','required': False}),
        }
        # Mensajes de error personalizados
        error_messages = {
            'fecha_nacimiento': {'required': 'Debes agregar la fecha de nacimiento.'},
            'telefono': {'required': 'Debes agregar la un numero de telefono.'},
            'direccion': {'required': 'Debes agregar la direccion.'},
            'usuario': {'required': 'Debes indicar el paciente.'},
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar usuarios para que solo aparezcan los pacientes
        self.fields['usuario'].queryset = User.objects.filter(rol='paciente')
        # Mostrar en el select el nombre completo y username
        self.fields['usuario'].label_from_instance = lambda obj: f"{obj.username} ({obj.first_name} {obj.last_name})"

    # Validación: fecha de nacimiento no puede ser futura
    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get('fecha_nacimiento')
        if fecha and fecha > date.today():
            raise forms.ValidationError("La fecha de nacimiento no puede ser futura.")
        return fecha

    # Validación: teléfono con formato 0000-0000
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '')
        if not re.match(r'^\d{4}-\d{4}$', telefono):
            raise forms.ValidationError("El teléfono debe tener el formato 0000-0000.")
        return telefono

    # Validación: dirección con mínimo 5 caracteres
    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion', '').strip()
        if len(direccion) < 5:
            raise forms.ValidationError("La dirección debe tener al menos 5 caracteres.")
        return direccion
    
    # Validación general para campos vacíos
    def clean(self):
        cleaned_data = super().clean()
        for field in ['usuario', 'fecha_nacimiento', 'telefono', 'direccion']:
            valor = cleaned_data.get(field)
            if not valor:
                self.add_error(field, f"El campo '{field}' no puede quedar vacío.")
        return cleaned_data


# ==============================
# FORMULARIO PARA MÉDICO
# ==============================
class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['usuario', 'matricula', 'telefono', 'especialidades']
        # Widgets para personalizar la apariencia de los campos
        widgets = {
            'matricula': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ejemplo: M-12345'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ejemplo: 7777-7777'
            }),
            'especialidades': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'usuario': forms.Select(attrs={'class': 'form-select'}),
        }
        # Mensajes de error personalizados
        error_messages = {
            'matricula': {'required': 'Debes agregar el numero de matricula.'},
            'telefono': {'required': 'Debes agregar la un numero de telefono.'},
            'especialidades': {'required': 'Debes indicar la especialidad.'},
            'usuario': {'required': 'Debes indicar el medico.'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar usuarios para que solo aparezcan los médicos
        self.fields['usuario'].queryset = User.objects.filter(rol='medico')
        self.fields['usuario'].label_from_instance = lambda obj: f"{obj.username} ({obj.first_name} {obj.last_name})"

    # Validación matrícula: entre 4 y 15 caracteres, letras, números o guiones
    def clean_matricula(self):
        matricula = self.cleaned_data.get('matricula', '').strip()
        if not re.match(r'^[A-Za-z0-9\-]{4,15}$', matricula):
            raise forms.ValidationError("La matrícula debe tener entre 4 y 15 caracteres (letras, números o guiones).")
        return matricula

    # Validación teléfono: formato 0000-0000
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '')
        if not re.match(r'^\d{4}-\d{4}$', telefono):
            raise forms.ValidationError("El teléfono debe tener el formato 0000-0000.")
        return telefono
    
    # Validación general: ningún campo vacío
    def clean(self):
        cleaned_data = super().clean()
        for campo, valor in cleaned_data.items():
            if not valor:
                raise forms.ValidationError(f"El campo '{campo}' no puede quedar vacío.")
        return cleaned_data


# ==============================
# FORMULARIO PARA CITA
# ==============================
class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['fecha_hora', 'motivo', 'estado', 'paciente', 'medico']
        # Widgets para personalizar la apariencia de los campos
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={
                'type': 'datetime-local', 
                'class': 'form-control'
            }),
            'motivo': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Describa brevemente el motivo de la cita'
            }),
            'estado': forms.Select(choices=[
                ('Pendiente', 'Pendiente'),
                ('Confirmada', 'Confirmada'),
                ('Cancelada', 'Cancelada'),
                ('Completada', 'Completada')
            ], attrs={'class': 'form-select'}),
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'medico': forms.Select(attrs={'class': 'form-select'}),
        }
        # Mensajes de error personalizados
        error_messages = {
            'fecha_hora': {'required': 'Debes indicar la fecha y la hora.'},
            'motivo': {'required': 'Debes agregar el mootivo.'},
            'estado': {'required': 'Debes indicar el estado de la cita.'},
            'paciente': {'required': 'Debes indicar el paciente.'},
            'medico': {'required': 'Debes indicar el medico.'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar nombres completos en el select de paciente
        self.fields['paciente'].queryset = Paciente.objects.select_related('usuario').all()
        self.fields['paciente'].label_from_instance = lambda obj: f"{obj.usuario.first_name} {obj.usuario.last_name}"
        
        # Mostrar nombres completos en el select de médico
        self.fields['medico'].queryset = Medico.objects.select_related('usuario').all()
        self.fields['medico'].label_from_instance = lambda obj: f"Dr(a). {obj.usuario.first_name} {obj.usuario.last_name}"

    # Validación fecha y hora: no puede ser pasada
    def clean_fecha_hora(self):
        fecha_hora = self.cleaned_data.get('fecha_hora')
        if fecha_hora is None:
            raise forms.ValidationError("Debe ingresar una fecha y hora para la cita.")
        if fecha_hora < timezone.now():
            raise forms.ValidationError("No puedes registrar una cita en una fecha u hora pasada.")
        return fecha_hora
 
    # Validación motivo: mínimo 5 caracteres
    def clean_motivo(self):
        motivo = self.cleaned_data.get('motivo', '').strip()
        if len(motivo) < 5:
            raise forms.ValidationError("El motivo de la cita debe tener al menos 5 caracteres.")
        return motivo
    
    # Validación general: ningún campo vacío
    def clean(self):
        cleaned_data = super().clean()
        for campo, valor in cleaned_data.items():
            if not valor:
                raise forms.ValidationError(f"El campo '{campo}' no puede quedar vacío.")
        return cleaned_data


# ==============================
# FORMULARIO PARA ESPECIALIDAD
# ==============================
class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ['nombre']
        # Widgets para personalizar la apariencia de los campos
        widgets = {
           'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ejemplo: Cardiología'
            }),
        }
        # Mensajes de error personalizados
        error_messages = {
            'nombre': {'required': 'Debes agregar el nombre de la especialidad.'},
        }
        
    # Validación del nombre de especialidad
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        if not nombre.replace(" ", "").isalpha():
            raise forms.ValidationError("El nombre solo puede contener letras y espacios.")
        # Validación para que no exista una especialidad con el mismo nombre
        if Especialidad.objects.filter(nombre__iexact=nombre).exists():
            raise forms.ValidationError("Ya existe una especialidad con este nombre.")
        return nombre
    
    # Validación general: ningún campo vacío
    def clean(self):
        cleaned_data = super().clean()
        for campo, valor in cleaned_data.items():
            if not valor:
                raise forms.ValidationError(f"El campo '{campo}' no puede quedar vacío.")
        return cleaned_data


# ==============================
# FORMULARIO PARA PERFIL DE PACIENTE
# ==============================
class PacientePerfilForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True,
        label='Fecha de nacimiento'
    )

    class Meta:
        model = Paciente
        fields = ['fecha_nacimiento', 'telefono', 'direccion']
        # Widgets para personalizar la apariencia de los campos
        widgets = {
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ejemplo: 7777-7777'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ejemplo: Calle 5, San Salvador'
            }),
        }
        # Mensajes de error personalizados
        error_messages = {
            'fecha_nacimiento': {'required': 'Debes agregar la fecha de nacimiento.'},
            'telefono': {'required': 'Debes agregar la un numero de telefono.'},
            'direccion': {'required': 'Debes agregar la direccion.'},
        }

    # Validar fecha de nacimiento: no puede ser futura
    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get('fecha_nacimiento')
        if not fecha:
            raise forms.ValidationError("La fecha de nacimiento es obligatoria.")
        if fecha > date.today():
            raise forms.ValidationError("La fecha de nacimiento no puede ser futura.")
        return fecha

    # Validar teléfono: formato 0000-0000
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '').strip()
        if not telefono:
            raise forms.ValidationError("El teléfono es obligatorio.")
        if not re.match(r'^\d{4}-\d{4}$', telefono):
            raise forms.ValidationError("El teléfono debe tener el formato 0000-0000.")
        return telefono

    # Validar dirección: mínimo 5 caracteres
    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion', '').strip()
        if not direccion:
            raise forms.ValidationError("La dirección no puede estar vacía.")
        if len(direccion) < 5:
            raise forms.ValidationError("La dirección debe tener al menos 5 caracteres.")
        return direccion

    # Validación general: ningún campo vacío
    def clean(self):
        cleaned_data = super().clean()
        for campo, valor in cleaned_data.items():
            if not valor:
                raise forms.ValidationError(f"El campo '{campo}' no puede quedar vacío.")
        return cleaned_data