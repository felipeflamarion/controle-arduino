# coding: utf-8
from django.shortcuts import render, HttpResponseRedirect
from django.core import urlresolvers
from django.views.generic import View
import datetime
from arduino.models import UtilizacaoModel, EquipamentoModel
from arduino.views import VisualizarEquipamento


def Emprestar(request, id_equipamento):
    equipamento = EquipamentoModel.objects.get(pk=id_equipamento)
    usuario = request.user
    quantidade_a_emprestar = request.POST.get('quantidade')
    if quantidade_a_emprestar <= equipamento.quantidade_disponivel:
        utilizacao = UtilizacaoModel(
            equipamento=equipamento,
            usuario=usuario,
            quantidade_utilizada=quantidade_a_emprestar
        )

        equipamento.quantidade_disponivel = int(equipamento.quantidade_disponivel) - int(quantidade_a_emprestar)
        equipamento.save()
        utilizacao.save()
        msg = "Empréstimo realizado com sucesso."
        cor_msg = "green"
    else:
        msg="Quantidade inválida."
        cor_msg="red"

    return VisualizarEquipamento(request, id_equipamento, msg=msg, cor_msg=cor_msg)


def Devolver(request, id_utilizacao):
    utilizacao = UtilizacaoModel.objects.get(pk=id_utilizacao)
    id_equipamento = utilizacao.equipamento.id

    if request.user == utilizacao.usuario:
        equipamento = utilizacao.equipamento
        equipamento.quantidade_disponivel = str(
            int(equipamento.quantidade_disponivel) + int(utilizacao.quantidade_utilizada))
        equipamento.save()
        utilizacao.ativo = False
        utilizacao.save()
    return VisualizarEquipamento(request, id_equipamento)