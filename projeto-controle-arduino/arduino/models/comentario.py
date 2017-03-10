#coding:utf-8
from django.db import models
from arduino.models import Usuario, Equipamento

class Comentario(models.Model):

    data = models.DateTimeField(auto_now=True, blank=True)
    mensagem = models.CharField(max_length=140)
    usuario = models.ForeignKey(Usuario)
    equipamento = models.ForeignKey(Equipamento)
