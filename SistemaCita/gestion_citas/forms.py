from django import forms
from .models import Paciente 
from .models import Medico
from .models import Cita
from .models import Especialidad
from django.contrib.auth import get_user_model
from django.utils import timezone
import re
from datetime import date

User = get_user_model()



# Formulario para Paciente
# FORMULARIO PACIENTE con validaciones
class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['usuario', 'fecha_nacimiento', 'telefono', 'direccion']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control',
                'max': '9999-12-31',
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
        error_messages = {
            'fecha_nacimiento': {'required': 'Debes agregar la fecha de nacimiento.'},
            'telefono': {'required': 'Debes agregar la un numero de telefono.'},
            'direccion': {'required': 'Debes agregar la direccion.'},
            'usuario': {'required': 'Debes indicar el paciente.'},
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].queryset = User.objects.filter(rol='paciente')
        self.fields['usuario'].label_from_instance = lambda obj: f"{obj.username} ({obj.first_name} {obj.last_name})"

    # 🔹 Validación personalizada: fecha de nacimiento
    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get('fecha_nacimiento')
        from datetime import date
        if fecha and fecha > date.today():
            raise forms.ValidationError("La fecha de nacimiento no puede ser futura.")
        return fecha

    # 🔹 Validación personalizada: teléfono
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '')
        import re
        if not re.match(r'^\d{4}-\d{4}$', telefono):
            raise forms.ValidationError("El teléfono debe tener el formato 0000-0000.")
        return telefono

    # 🔹 Validación personalizada: dirección
    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion', '').strip()
        if len(direccion) < 5:
            raise forms.ValidationError("La dirección debe tener al menos 5 caracteres.")
        return direccion
    
    def clean(self):
     cleaned_data = super().clean()

     for field in ['usuario', 'fecha_nacimiento', 'telefono', 'direccion']:
        valor = cleaned_data.get(field)
        if not valor:
            self.add_error(field, f"El campo '{field}' no puede quedar vacío.")

     return cleaned_data
# Formulario para Medico
# FORMULARIO MÉDICO con validaciones
class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['usuario', 'matricula', 'telefono', 'especialidades']
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
        error_messages = {
            'matricula': {'required': 'Debes agregar el numero de matricula.'},
            'telefono': {'required': 'Debes agregar la un numero de telefono.'},
            'especialidades': {'required': 'Debes indicar la especialidad.'},
            'usuario': {'required': 'Debes indicar el medico.'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].queryset = User.objects.filter(rol='medico')
        self.fields['usuario'].label_from_instance = lambda obj: f"{obj.username} ({obj.first_name} {obj.last_name})"

    # 🔹 Validación matrícula
    def clean_matricula(self):
        matricula = self.cleaned_data.get('matricula', '').strip()
        import re
        if not re.match(r'^[A-Za-z0-9\-]{4,15}$', matricula):
            raise forms.ValidationError("La matrícula debe tener entre 4 y 15 caracteres (letras, números o guiones).")
        return matricula

    # 🔹 Validación teléfono
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '')
        import re
        if not re.match(r'^\d{4}-\d{4}$', telefono):
            raise forms.ValidationError("El teléfono debe tener el formato 0000-0000.")
        return telefono
    
    def clean(self):
        cleaned_data = super().clean()
        for campo, valor in cleaned_data.items():
            if not valor:
                raise forms.ValidationError(f"El campo '{campo}' no puede quedar vacío.")
        return cleaned_data
    
# Formulario para Cita
class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['fecha_hora', 'motivo', 'estado', 'paciente', 'medico']
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
        error_messages = {
            'fecha_hora': {'required': 'Debes indicar la fecha y la hora.'},
            'motivo': {'required': 'Debes agregar el mootivo.'},
            'estado': {'required': 'Debes indicar el estado de la cita.'},
            'paciente': {'required': 'Debes indicar el paciente.'},
            'medico': {'required': 'Debes indicar el medico.'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Paciente.objects.select_related('usuario').all()
        self.fields['paciente'].label_from_instance = lambda obj: f"{obj.usuario.first_name} {obj.usuario.last_name}"
        
        self.fields['medico'].queryset = Medico.objects.select_related('usuario').all()
        self.fields['medico'].label_from_instance = lambda obj: f"Dr(a). {obj.usuario.first_name} {obj.usuario.last_name}"

    # 🔹 Validación de fecha y hora (no pasada)
    def clean_fecha_hora(self):
     fecha_hora = self.cleaned_data.get('fecha_hora')

     # Si el campo está vacío, no seguir comparando
     if fecha_hora is None:
        raise forms.ValidationError("Debe ingresar una fecha y hora para la cita.")

    # Validar que la fecha no sea pasada
     if fecha_hora < timezone.now():
        raise forms.ValidationError("No puedes registrar una cita en una fecha u hora pasada.")

     return fecha_hora
 
    # 🔹 Validación motivo
    def clean_motivo(self):
        motivo = self.cleaned_data.get('motivo', '').strip()
        if len(motivo) < 5:
            raise forms.ValidationError("El motivo de la cita debe tener al menos 5 caracteres.")
        return motivo
    
    def clean(self):
        cleaned_data = super().clean()
        for campo, valor in cleaned_data.items():
            if not valor:
                raise forms.ValidationError(f"El campo '{campo}' no puede quedar vacío.")
        return cleaned_data

# Formulario para Especialidad
class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ['nombre']
        widgets = {
           'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ejemplo: Cardiología'
            }),
        }
        error_messages = {
            'nombre': {'required': 'Debes agregar el nombre de la especialidad.'},
        }
        
       # 🔹 Validación del nombre
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        if not nombre.replace(" ", "").isalpha():
            raise forms.ValidationError("El nombre solo puede contener letras y espacios.")
        if Especialidad.objects.filter(nombre__iexact=nombre).exists():
            raise forms.ValidationError("Ya existe una especialidad con este nombre.")
        return nombre
    
    def clean(self):
        cleaned_data = super().clean()
        for campo, valor in cleaned_data.items():
            if not valor:
                raise forms.ValidationError(f"El campo '{campo}' no puede quedar vacío.")
        return cleaned_data
    
  
class PacientePerfilForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True,
        label='Fecha de nacimiento'
    )

    class Meta:
        model = Paciente
        fields = ['fecha_nacimiento', 'telefono', 'direccion']
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
        error_messages = {
            'fecha_nacimiento': {'required': 'Debes agregar la fecha de nacimiento.'},
            'telefono': {'required': 'Debes agregar la un numero de telefono.'},
            'direccion': {'required': 'Debes agregar la direccion.'},
        }

    # 🔹 Validar fecha de nacimiento
    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get('fecha_nacimiento')
        if not fecha:
            raise forms.ValidationError("La fecha de nacimiento es obligatoria.")
        if fecha > date.today():
            raise forms.ValidationError("La fecha de nacimiento no puede ser futura.")
        return fecha

    # 🔹 Validar teléfono
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '').strip()
        if not telefono:
            raise forms.ValidationError("El teléfono es obligatorio.")
        if not re.match(r'^\d{4}-\d{4}$', telefono):
            raise forms.ValidationError("El teléfono debe tener el formato 0000-0000.")
        return telefono

    # 🔹 Validar dirección
    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion', '').strip()
        if not direccion:
            raise forms.ValidationError("La dirección no puede estar vacía.")
        if len(direccion) < 5:
            raise forms.ValidationError("La dirección debe tener al menos 5 caracteres.")
        return direccion

    # 🔹 Validación general
    def clean(self):
        cleaned_data = super().clean()
        for campo, valor in cleaned_data.items():
            if not valor:
                raise forms.ValidationError(f"El campo '{campo}' no puede quedar vacío.")
        return cleaned_data
        
        



