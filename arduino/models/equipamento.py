# coding: utf-8
from django.db import models
from arduino.models import CategoriaModel


class EquipamentoModel(models.Model):
    descricao = models.CharField(max_length=75, unique=True, null=False)
    observacao = models.TextField(max_length=400, blank=True)
    quantidade_total = models.CharField(max_length=3, default=0)
    quantidade_disponivel = models.CharField(max_length=3, default=0, blank=True)
    ativo = models.BooleanField(default=True)
    data_alteracao = models.DateTimeField()
    foto = models.ImageField(upload_to='equipamentos', blank=True)
    categoria = models.ForeignKey(CategoriaModel)

    def __unicode__(self):
        return u'%s' %self.descricao

    def __str__(self):
        return u'%s' %self.descricao

    class Meta:
        verbose_name = u"Equipamento"
        verbose_name_plural = u"Equipamentos"
