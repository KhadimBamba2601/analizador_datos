from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import FormularioConjuntoDatos
from .models import ConjuntoDatos
import os
import django
from django.contrib.auth.models import User, Group
from django.conf import settings

class LoginUsuario(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = False

    def get_success_url(self):
        messages.success(self.request, "Inicio de sesión exitoso")
        return self.request.GET.get('next', '/')

    def form_invalid(self, form):
        messages.error(self.request, "Credenciales incorrectas. Por favor, intenta de nuevo.")
        return super().form_invalid(form)

def es_analista_o_admin(user):
    return user.is_superuser or user.groups.filter(name__in=['Administradores', 'Analistas']).exists()

@login_required
@user_passes_test(es_analista_o_admin)
def inicio(request):
    return render(request, 'inicio.html')

@login_required
@user_passes_test(es_analista_o_admin)
def subir_conjunto_datos(request):
    if request.method == 'POST':
        form = FormularioConjuntoDatos(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            if not archivo.name.endswith('.csv'):
                messages.error(request, "Solo se permiten archivos CSV")
                return render(request, 'subir_conjunto.html', {'form': form})
            if archivo.size > 10 * 1024 * 1024:
                messages.error(request, "Archivo demasiado grande (máximo 10MB)")
                return render(request, 'subir_conjunto.html', {'form': form})
            conjunto = ConjuntoDatos(
                usuario=request.user,
                archivo=archivo,
                nombre=archivo.name
            )
            conjunto.save()
            messages.success(request, "Archivo subido correctamente")
            return redirect('inicio')
    else:
        form = FormularioConjuntoDatos()
    return render(request, 'subir_conjunto.html', {'form': form})

# Agregar automáticamente el superusuario a los grupos requeridos
if django.apps.apps.ready:
    try:
        superuser = User.objects.filter(is_superuser=True).first()
        if superuser:
            g1, _ = Group.objects.get_or_create(name='Administradores')
            g2, _ = Group.objects.get_or_create(name='Analistas')
            superuser.groups.add(g1, g2)
    except Exception as e:
        pass  # Evita errores en migraciones o cuando la base de datos no está lista