# coding: utf-8
from django.shortcuts import render
from arduino.models import EquipamentoModel


def Painel(request, msg=None, cor_msg=None):
    context_dict = {}
    equipamentos = EquipamentoModel.objects.order_by('-data_registro', '-id')[:10]
    context_dict['msg'] = msg
    context_dict['cor_msg'] = cor_msg
    context_dict['dados'] = equipamentos
    return render(request, 'painel.html', context_dict)
