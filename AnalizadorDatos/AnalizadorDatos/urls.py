from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Analisis.views import LoginUsuario, inicio, subir_conjunto_datos
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginUsuario.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', inicio, name='inicio'),
    path('subir/', subir_conjunto_datos, name='subir_conjunto_datos'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)