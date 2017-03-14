#coding:utf-8
from django.shortcuts import render, HttpResponseRedirect
from django.core import urlresolvers
from django.views.generic import View
from arduino.models import Equipamento, Comentario

class Comentar(View):

    def post(self, request, id_equipamento):
        try:
            usuario = request.user
            equipamento = Equipamento.objects.get(pk=id_equipamento)
            mensagem = request.POST.get('mensagem')

            comentario = Comentario(
                usuario=usuario,
                equipamento=equipamento,
                mensagem=mensagem
            )
            comentario.save()
        except:
            print("Houve erro durante o envio do comentário!")
        return HttpResponseRedirect(urlresolvers.reverse('visualizar_equipamento', args=({id_equipamento: equipamento.id})))
