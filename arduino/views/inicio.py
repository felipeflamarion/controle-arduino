# coding: utf-8
from django.shortcuts import render, HttpResponseRedirect
from django.core import urlresolvers
from django.views.generic import View


class InicioView(View):
    template = 'inicio.html'

    def get(self, request):
        context_dict = {}
        if request.user.is_authenticated:
            return HttpResponseRedirect(urlresolvers.reverse('painel'))
        return render(request, self.template, context_dict)
