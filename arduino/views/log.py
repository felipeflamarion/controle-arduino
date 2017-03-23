# coding: utf-8
from django.shortcuts import render, HttpResponseRedirect
from django.core import urlresolvers
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View


class LoginView(View):
    template = 'inicio.html'

    def post(self, request):
        context_dict = {}

        username = request.POST.get('username')
        password = request.POST.get('password')

        usuario = authenticate(username=username, password=password)

        if usuario:
            if usuario.is_active:
                login(request, usuario)
                return HttpResponseRedirect(urlresolvers.reverse('painel'))
            else:
                context_dict['login_error'] = u'Usuário desativado!'
        else:
            context_dict['login_error'] = u'Usuário ou Senha inválidos!'

        return render(request, self.template, context_dict)


def Logout(request):
    logout(request)
    return HttpResponseRedirect(urlresolvers.reverse('inicio'))
