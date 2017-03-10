#coding:utf-8
from django.db import models

class Categoria(models.Model):

    descricao = models.CharField(max_length=25, unique=True)

    def __unicode__(self):
        return u'%s' %self.descricao

    class Meta:
        ordering = ['descricao']
