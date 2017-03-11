#coding:utf-8
from django.db import models

class Caixa(models.Model):

    descricao = models.CharField(max_length=25, unique=True)
    observacao = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return u'%s' %self.descricao

    class Meta:
        ordering = ['descricao']
