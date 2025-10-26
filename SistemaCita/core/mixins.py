from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

class RolRequiredMixin(LoginRequiredMixin):
    rol_permitido = None        # Para un solo rol
    roles_permitidos = []       # Para varios roles

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        rol_usuario = getattr(request.user, 'rol', None)

        # Verifica un solo rol
        if self.rol_permitido and rol_usuario != self.rol_permitido:
            return redirect('home')

        # Verifica múltiples roles
        if self.roles_permitidos and rol_usuario not in self.roles_permitidos:
            return redirect('home')

        return super().dispatch(request, *args, **kwargs)