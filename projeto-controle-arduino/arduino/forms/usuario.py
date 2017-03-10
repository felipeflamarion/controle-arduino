#coding:utf-8
from django import forms
from arduino.models import Usuario

class UsuarioForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Usuario
        fields = ('first_name', 'username', 'email', 'password')