from django.urls import path
from .views import LoginUsuario, inicio, subir_conjunto_datos
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', inicio, name='inicio'),
    path('login/', LoginUsuario.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('subir/', subir_conjunto_datos, name='subir_conjunto_datos'),
]