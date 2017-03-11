#coding:utf-8
from django import forms
from arduino.models import Equipamento

class EquipamentoForm(forms.ModelForm):

    class Meta:
        model = Equipamento
        fields = ('descricao', 'observacao', 'quantidade_total', 'foto', 'caixa', 'categoria')