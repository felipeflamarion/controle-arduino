#coding:utf-8
from django.shortcuts import render, HttpResponseRedirect
from django.core import urlresolvers
from django.views.generic import View

from arduino.forms import UsuarioForm

class CadastroUsuario(View):

    context = {}
    template = 'cadastro_usuario.html'

    def get(self, request):
        self.context['usuario_form'] = UsuarioForm
        return render(request, self.template, self.context)

    def post(self, request):
        usuario_form = UsuarioForm(request.POST)

        if usuario_form.is_valid():
            usuario = usuario_form.save()
            usuario.set_password(usuario.password)
            usuario.save()
            self.context['cadastro_realizado'] = True
        else:
            self.context['usuario_form'] = usuario_form

        return render(request, self.template, self.context)