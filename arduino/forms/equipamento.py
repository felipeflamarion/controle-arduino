# coding: utf-8
from django import forms
from arduino.models import EquipamentoModel


class EquipamentoForm(forms.ModelForm):

    class Meta:
        model = EquipamentoModel
        fields = ('descricao', 'observacao', 'foto', 'local', 'categoria')
