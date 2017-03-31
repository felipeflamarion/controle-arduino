# coding: utf-8
from django.shortcuts import render
from arduino.models import EquipamentoModel
from arduino.views import pagination


def Painel(request, msg=None, cor_msg=None):
    context_dict = {}
    equipamentos = EquipamentoModel.objects.order_by('-data_registro', '-id')[:10]
    context_dict['msg'] = msg
    context_dict['cor_msg'] = cor_msg
    print(equipamentos)
    dados, page_range, ultima = pagination(equipamentos, request.GET.get('page'))
    # context_dict['dados'] = dados
    # context_dict['page_range'] = page_range
    # context_dict['ultima'] = ultima
    return render(request, 'painel.html', context_dict)
