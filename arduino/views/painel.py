# coding: utf-8
from django.shortcuts import render
from django.views.generic import View
from arduino.models import EquipamentoModel


class PainelView(View):
    template = 'painel.html'

    def get(self, request):
        context_dict = {
            'equipamentos_recentemente_cadastrados': EquipamentoModel.objects.order_by('-data_registro', '-id')[:10]}
        return render(request, self.template, context_dict)
