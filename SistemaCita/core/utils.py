from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

def crear_admin():
    User = get_user_model()

    # Crear grupos si no existen
    grupos = {}
    for nombre in ["Administrador", "Medico", "Paciente"]:
        grupo, _ = Group.objects.get_or_create(name=nombre)
        grupos[nombre] = grupo

    # Crear usuario admin si no existe
    if not User.objects.filter(username="admin").exists():
        admin = User(username="admin", email="admin@midominio.com")
        admin.set_password("admin123")  # contraseña
        admin.is_superuser = True
        admin.is_staff = True
        admin.is_active = True
        admin.rol = "admin"  # tu campo rol
        admin.save()
        admin.groups.add(grupos["Administrador"])
        print("✅ Usuario admin creado automáticamente")
    else:
        print("⚠ Usuario admin ya existe")