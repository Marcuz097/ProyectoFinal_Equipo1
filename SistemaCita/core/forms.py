from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from gestion_citas.models import Paciente
from gestion_citas.models import Cita
from gestion_citas.models import Medico
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
import re


class RegistroForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=False,
        label='Nombre',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: Juan'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        label='Apellido',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: Pérez'})
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'}),
        }
        error_messages = {
            'username': {
                'required': "El Usuario es obligatorio.",
            }
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = 'paciente'  # 🔹 Fuerza que todos los registros sean pacientes
        if commit:
            user.save()
            # 🔹 Crea también el perfil de paciente
            Paciente.objects.create(usuario=user)
        return user

    # 🔹 Validación del nombre
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '').strip()
        if not first_name:
            raise forms.ValidationError("El nombre es obligatorio.")
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$', first_name):
            raise forms.ValidationError("El nombre solo puede contener letras y espacios.")
        if len(first_name) < 2:
            raise forms.ValidationError("El nombre debe tener al menos 2 caracteres.")
        return first_name

    # 🔹 Validación del apellido
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '').strip()
        if not last_name:
            raise forms.ValidationError("El apellido es obligatorio.")
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$', last_name):
            raise forms.ValidationError("El apellido solo puede contener letras y espacios.")
        if len(last_name) < 2:
            raise forms.ValidationError("El apellido debe tener al menos 2 caracteres.")
        return last_name

    # 🔹 Validación del nombre de usuario
    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if not username:
            raise forms.ValidationError("El nombre de usuario es obligatorio.")
        if len(username) < 4:
            raise forms.ValidationError("El nombre de usuario debe tener al menos 4 caracteres.")
        if re.search(r'\s', username):
            raise forms.ValidationError("El nombre de usuario no puede contener espacios.")
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username

    # 🔹 Validación del correo electrónico
    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if not email:
            raise forms.ValidationError("El correo electrónico es obligatorio.")
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise forms.ValidationError("Ingrese un correo electrónico válido.")
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

    # 🔹 Validación del rol
    def clean_rol(self):
        rol = self.cleaned_data.get('rol')
        if not rol:
            raise forms.ValidationError("Debe seleccionar un tipo de usuario.")
        return rol

    # 🔹 Validación de las contraseñas y campos vacíos
    def clean_password1(self):
        password = self.cleaned_data.get('password1', '')

        if not password:
            raise forms.ValidationError("La contraseña es obligatoria.")
        if len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("La contraseña debe contener al menos una letra mayúscula (A-Z).")
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError("La contraseña debe contener al menos una letra minúscula (a-z).")
        if not re.search(r'\d', password):
            raise forms.ValidationError("La contraseña debe contener al menos un número (0-9).")
        # Opcional: exigir un símbolo especial
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError("La contraseña debe contener al menos un carácter especial (!@#$%^&* etc.).")

        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        
        for campo, valor in cleaned_data.items():
            if valor in [None, '']:
                raise forms.ValidationError(f"El campo '{campo}' no puede quedar vacío.")
        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.first_name = self.cleaned_data.get('first_name', '').strip()
        usuario.last_name = self.cleaned_data.get('last_name', '').strip()
        if commit:
            usuario.save()
        return usuario

class PacienteCitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['medico', 'fecha_hora', 'motivo']  # paciente y estado se asignan automáticamente
        widgets = {
            'medico': forms.Select(attrs={'class': 'form-select'}),
            'fecha_hora': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe el motivo de tu cita'}),
        }
        error_messages = {
            'medico': {'required': 'Debes seleccionar un médico.'},
            'fecha_hora': {'required': 'Debes seleccionar la fecha y hora de la cita.'},
            'motivo': {'required': 'Debes indicar el motivo de la cita.'},
        }

    # 🔹 Validación del médico
    def clean_medico(self):
        medico = self.cleaned_data.get('medico')
        if not medico:
            raise forms.ValidationError("Debes seleccionar un médico.")
        return medico

    # 🔹 Validación de fecha y hora
    def clean_fecha_hora(self):
        fecha_hora = self.cleaned_data.get('fecha_hora')
        if not fecha_hora:
            raise forms.ValidationError("Debes seleccionar la fecha y hora de la cita.")
        if fecha_hora < timezone.now():  # ⚡ usar timezone.now() en vez de datetime.datetime.now()
            raise forms.ValidationError("La fecha y hora de la cita no puede ser en el pasado.")
        return fecha_hora

    # 🔹 Validación del motivo
    def clean_motivo(self):
        motivo = self.cleaned_data.get('motivo', '').strip()
        if not motivo:
            raise forms.ValidationError("Debes indicar el motivo de la cita.")
        if len(motivo) < 5:
            raise forms.ValidationError("El motivo debe tener al menos 5 caracteres.")
        return motivo
    
class MedicoRegistroForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput
    )

    class Meta:
        model = Usuario
        required = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
          'username': 'Nombre de usuario',
          'first_name': 'Nombre',
          'last_name': 'Apellido',
          'email': 'Correo electrónico',
          
    }
    widgets = {
            'username': forms.TextInput(attrs={'required': False}),
            'first_name': forms.TextInput(attrs={'required': False}),
            'last_name': forms.TextInput(attrs={'required': False}),
            'email': forms.EmailInput(attrs={'required': False}),
        }
    error_messages = {
            'username': {
                'unique': 'Este nombre de usuario ya existe'
            },
            'email': {
                'invalid': 'Ingrese un correo válido'
            }
        }

    
    def clean_username(self):
     username = self.cleaned_data.get('username')
     if not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise forms.ValidationError("El nombre de usuario solo puede contener letras, números y guiones bajos")
     return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2
    
    def clean(self):
     cleaned_data = super().clean()

     campos_obligatorios = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

     for campo in campos_obligatorios:
        valor = cleaned_data.get(campo)
        if not valor:
            self.add_error(campo, 'Este campo es obligatorio')

     return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.rol = 'medico'  # 👈 fuerza el rol de médico
        user.is_active = True
        if commit:
            user.save()
        return user

    