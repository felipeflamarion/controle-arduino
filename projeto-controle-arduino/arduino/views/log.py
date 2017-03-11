#coding:utf-8
from django.shortcuts import render, HttpResponseRedirect
from django.core import urlresolvers
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View

class Login(View):

    context = {}

    def post(self, request):

        username = request.POST.get('username')
        password = request.POST.get('password')
        print('\nUsername: %s\nPassword: %s' % (username, password))

        usuario = authenticate(username=username, password=password)

        if usuario:
            if usuario.is_active:
                login(request, usuario)
                return HttpResponseRedirect(urlresolvers.reverse('inicio'))
            else:
                self.context['login_error'] = u'Usuário desativado!'
        else:
            self.context['login_error'] = u'Usuário ou Senha inválidos!'

        return render(request, 'inicio.html', self.context)