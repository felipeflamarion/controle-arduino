# coding: utf-8
from django.db import models
from arduino.models import Usuario, EquipamentoModel


class UtilizacaoModel(models.Model):
    data_retirada = models.DateTimeField(auto_now_add=True, blank=True)
    data_devolucao = models.DateTimeField(auto_now_add=True, blank=True)
    quantidade_utilizada = models.CharField(max_length=3, default=1)
    usuario = models.ForeignKey(Usuario, null=False)
    equipamento = models.ForeignKey(EquipamentoModel, null=False)

    ativo = models.BooleanField(default=True)
    ''' RETIRAR APÓS CRIAR VERIFICAÇÃO DA INATIVIDADE DENTRO DO INTERVALO DA DATA DE RETIRADA E DE DEVOLUÇÃO '''

    class Meta:
        verbose_name = u"Utilização"
        verbose_name_plural = u"Utilizações"