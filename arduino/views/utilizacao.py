# coding: utf-8
from django.shortcuts import render, HttpResponseRedirect
from django.core import urlresolvers
from django.views.generic import View
import datetime
from arduino.models import UtilizacaoModel, EquipamentoModel


class EmprestarView(View):

    def post(self, request, id_equipamento):
        try:
            equipamento = EquipamentoModel.objects.get(pk=id_equipamento)
            usuario = request.user
            quantidade_utilizada = request.POST.get('quantidade')
            utilizacao = UtilizacaoModel(
                equipamento=equipamento,
                usuario=usuario,
                quantidade_utilizada=quantidade_utilizada
            )

            equipamento.quantidade_disponivel = int(equipamento.quantidade_disponivel) - int(quantidade_utilizada)
            equipamento.save()
            utilizacao.save()
        except:
             print("Houveram erros durante o empréstimo do equipamento")

        return HttpResponseRedirect(urlresolvers.reverse('visualizar_equipamento', args=({id_equipamento: equipamento.id})))


class DevolverView(View):

    def get(self, request, id_utilizacao):
        try:
            utilizacao = UtilizacaoModel.objects.get(pk=id_utilizacao)
            id_equipamento = utilizacao.equipamento.id

            if request.user == utilizacao.usuario: # and utilizacao.ativo:
                #utilizacao.data_devolucao = datetime.datetime.now()
                equipamento = utilizacao.equipamento
                equipamento.quantidade_disponivel = str(int(equipamento.quantidade_disponivel) + int(utilizacao.quantidade_utilizada))
                equipamento.save()
                utilizacao.ativo = False
                utilizacao.save()
            return HttpResponseRedirect(urlresolvers.reverse('visualizar_equipamento', args=({id_equipamento: id_equipamento})))
        except:
            pass
        return HttpResponseRedirect(urlresolvers.reverse('painel'))
