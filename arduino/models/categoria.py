# coding: utf-8
from django.db import models


class CategoriaModel(models.Model):
    descricao = models.CharField(max_length=25, unique=True)

    def __unicode__(self):
        return u'%s' % self.descricao

    def __str__(self):
        return u'%s' % self.descricao

    class Meta:
        ordering = ['descricao']
        verbose_name = u"Categoria"
        verbose_name_plural = u"Categorias"
