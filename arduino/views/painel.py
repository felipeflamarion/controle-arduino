# coding: utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from arduino.models import EquipamentoModel


@login_required
def Painel(request, msg=None, cor_msg=None):
    context_dict = {}
    equipamentos = EquipamentoModel.objects.order_by('-data_registro', '-id')[:5]
    context_dict['msg'] = msg
    context_dict['cor_msg'] = cor_msg
    context_dict['dados'] = equipamentos
    return render(request, 'painel.html', context_dict)
