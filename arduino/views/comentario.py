# coding: utf-8
from django.shortcuts import render, HttpResponseRedirect
from django.core import urlresolvers
from django.views.generic import View
from arduino.models import EquipamentoModel, ComentarioModel


class ComentarView(View):
    def post(self, request, id_equipamento=None):
        usuario = request.user
        equipamento = EquipamentoModel.objects.get(pk=id_equipamento)
        mensagem = request.POST['mensagem']

        comentario = ComentarioModel(
            usuario=usuario,
            equipamento=equipamento,
            mensagem=mensagem
        )
        comentario.save()

        return HttpResponseRedirect(urlresolvers.reverse('visualizar_equipamento', args=[id_equipamento]))
