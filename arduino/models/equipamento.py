#coding:utf-8
from django.db import models
from arduino.models import Caixa, Categoria

class Equipamento(models.Model):

    descricao = models.CharField(max_length=75, unique=True)
    observacao = models.CharField(max_length=150, blank=True)
    quantidade_total = models.IntegerField(default=0)
    quantidade_disponivel = models.IntegerField(default=0, blank=True)
    data_registro = models.DateField(auto_now=True, blank=True)
    foto = models.ImageField(upload_to='equipamentos', blank=True)
    caixa = models.ForeignKey(Caixa, blank=True, null=True)
    categoria = models.ForeignKey(Categoria)

    def __unicode__(self):
        return u'%s' %self.descricao
