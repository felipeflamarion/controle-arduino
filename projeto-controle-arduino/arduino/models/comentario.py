#coding:utf-8
from django.db import models
from arduino.models import User, Equipamento

class Comentario(models.Model):

    data = models.DateTimeField(auto_now=True, blank=True)
    mensagem = models.CharField(max_length=140)
    usuario = models.ForeignKey(User)
    equipamento = models.ForeignKey(Equipamento)
