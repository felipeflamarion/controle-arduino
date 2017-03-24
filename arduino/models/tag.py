# coding: utf-8
from django.db import models
from arduino.models import EquipamentoModel


class TagModel(models.Model):
    descricao = models.CharField(max_length=25, unique=True)
    equipamento = models.ManyToManyField(EquipamentoModel, blank=True)

    def __unicode__(self):
        return u'%s' %self.descricao

    def __str__(self):
        return u'%s' %self.descricao

    class Meta:
        ordering = ['descricao']
        verbose_name = u"Local"
        verbose_name_plural = u"Locais"
