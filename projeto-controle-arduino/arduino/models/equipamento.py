#coding:utf-8
from django.db import models
from arduino.models import Caixa, Categoria

class Equipamento(models.Model):

    descricao = models.CharField(max_length=75, unique=True)
    observacao = models.CharField(max_length=150, blank=True)
    quantidade = models.IntegerField(default=0)
    foto = models.ImageField(upload_to='equipamentos', blank=True)

    def __unicode__(self):
        return u'%s' %self.descricao
