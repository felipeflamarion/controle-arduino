# coding: utf-8
from django.shortcuts import render, HttpResponseRedirect
from django.core import urlresolvers
from django.contrib.auth import authenticate, login, logout


def Login(request):
    context_dict = {}

    username = request.POST.get('username')
    password = request.POST.get('password')

    usuario = authenticate(username=username, password=password)

    if usuario:
        if usuario.is_active:
            login(request, usuario)
            return HttpResponseRedirect(urlresolvers.reverse('painel'))
        else:
            print(u'Usuário desativado!')
    else:
        print(u'Usuário ou Senha inválidos!')

    return render(request, 'inicio.html', context_dict)


def Logout(request):
    logout(request)
    return HttpResponseRedirect(urlresolvers.reverse('inicio'))
