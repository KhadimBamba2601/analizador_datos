from django.db import models
from django.contrib.auth.models import User
from encrypted_fields import fields

class ConjuntoDatos(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='datasets/')
    subido_en = models.DateTimeField(auto_now_add=True)
    nombre = fields.EncryptedCharField(max_length=255)

class ResultadoAnalisis(models.Model):
    conjunto_datos = models.ForeignKey(ConjuntoDatos, on_delete=models.CASCADE)
    estadisticas = models.JSONField()
    grafico = models.ImageField(upload_to='plots/', null=True)