#coding:utf-8
from django.shortcuts import render
from django.views.generic import View
from arduino.models import Equipamento

class Painel(View):

    template = 'painel.html'

    def get(self, request):
        context = {}
        context['equipamentos_recentemente_cadastrados'] = Equipamento.objects.order_by('-data_registro')[:5]
        return render(request, self.template, context)