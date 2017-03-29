# coding: utf-8
from django.shortcuts import render, HttpResponseRedirect
from django.core import urlresolvers


def Inicio(request):
    context_dict = {}
    if request.user.is_authenticated:
        return HttpResponseRedirect(urlresolvers.reverse('painel'))
    return render(request, 'inicio.html', context_dict)
