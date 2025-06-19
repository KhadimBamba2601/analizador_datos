from django.contrib.auth.views import LoginView

class LoginUsuario(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def inicio(request):
    return render(request, 'inicio.html')