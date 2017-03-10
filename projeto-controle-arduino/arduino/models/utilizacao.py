#coding:utf-8
from django.db import models
from arduino.models import Usuario, Equipamento

class Utilizacao(models.Model):

    data_retirada = models.DateTimeField(auto_now_add=True, blank=True)
    data_devolucao = models.DateTimeField(auto_now_add=True, blank=True)
    usuario = models.ForeignKey(Usuario)
    equipamento = models.ForeignKey(Equipamento)

    class Meta:
        verbose_name_plural = u'Utilizações'
