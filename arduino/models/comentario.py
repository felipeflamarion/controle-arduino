# coding: utf-8
from django.db import models
from arduino.models import Usuario, EquipamentoModel


class ComentarioModel(models.Model):
    data = models.DateTimeField(auto_now=True, blank=True)
    mensagem = models.CharField(max_length=140)
    usuario = models.ForeignKey(Usuario)
    equipamento = models.ForeignKey(EquipamentoModel)

    def __unicode__(self):
        return u'%s' % self.mensagem

    def __str__(self):
        return u'%s' % self.mensagem

    class Meta:
        ordering = ['data']
        verbose_name = u"Comentário"
        verbose_name_plural = u"Comentários"
