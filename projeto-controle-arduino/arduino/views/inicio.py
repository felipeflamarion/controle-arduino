#coding:utf-8
from django.shortcuts import render, HttpResponseRedirect
from django.core import urlresolvers
from django.views.generic import View

class InicioView(View):

    context = {}
    template = 'inicio.html'

    def get(self, request):
        return render(request, self.template, self.context)
