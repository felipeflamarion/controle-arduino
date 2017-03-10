#coding:utf-8
from django import forms


class UsuarioForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'username', 'email', 'password')