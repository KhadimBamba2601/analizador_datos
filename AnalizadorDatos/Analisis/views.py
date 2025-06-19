from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import FormularioConjuntoDatos
from .models import ConjuntoDatos
from django.http import HttpResponse
import os

class LoginUsuario(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = False  # Cambia a False

def es_analista_o_admin(user):
    return user.groups.filter(name__in=['Administradores', 'Analistas']).exists()

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
            # Validaciones de seguridad
            if not archivo.name.endswith('.csv'):
                return HttpResponse("Solo se permiten archivos CSV", status=400)
            if archivo.size > 10 * 1024 * 1024:  # 10MB
                return HttpResponse("Archivo demasiado grande", status=400)
            # Guardar dataset
            conjunto = ConjuntoDatos(
                usuario=request.user,
                archivo=archivo,
                nombre=archivo.name
            )
            conjunto.save()
            return redirect('inicio')
    else:
        form = FormularioConjuntoDatos()
    return render(request, 'subir_conjunto.html', {'form': form})