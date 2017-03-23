# coding: utf-8
from django.shortcuts import render, HttpResponseRedirect
from django.core import urlresolvers
from django.views.generic import View
from arduino.forms import UsuarioForm


class CadastroUsuarioView(View):
    template = 'cadastro_usuario.html'

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(urlresolvers.reverse('painel'))

        context_dict = {'usuario_form': UsuarioForm}
        return render(request, self.template, context_dict)

    def post(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(urlresolvers.reverse('painel'))

        context_dict = {}
        usuario_form = UsuarioForm(request.POST)

        if usuario_form.is_valid():
            usuario = usuario_form.save()
            usuario.set_password(usuario.password)
            usuario.save()
            context_dict['cadastro_realizado'] = True
        else:
            context_dict['usuario_form'] = usuario_form
        return render(request, self.template, context_dict)
