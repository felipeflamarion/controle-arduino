#coding:utf-8
from django.shortcuts import render, HttpResponseRedirect
from django.core import urlresolvers
from django.views.generic import View
from arduino.models import Utilizacao, Equipamento

class Emprestar(View):

    def post(self, request, id_equipamento):

        context = {}

        #try:
        equipamento = Equipamento.objects.get(pk=id_equipamento)

        print(equipamento.quantidade_disponivel)

        usuario = request.user
        quantidade_utilizada = request.POST.get('quantidade')
        utilizacao = Utilizacao(
            equipamento=equipamento,
            usuario=usuario,
            quantidade_utilizada=quantidade_utilizada
        )


        equipamento.quantidade_disponivel = int(equipamento.quantidade_disponivel) - int(quantidade_utilizada)
        print(equipamento.quantidade_disponivel)
        equipamento.save()
        utilizacao.save()

        # except:
        #     print("Houveram erros durante o empréstimo do equipamento")

        return HttpResponseRedirect(urlresolvers.reverse('visualizar_equipamento', args=({id_equipamento: equipamento.id})))
