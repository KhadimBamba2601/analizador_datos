from django import forms

class FormularioConjuntoDatos(forms.Form):
    archivo = forms.FileField(label='Selecciona un archivo CSV')