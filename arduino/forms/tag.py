#coding:utf-8
from django import forms
from arduino.models import TagModel

class TagForm(forms.ModelForm):

    descricao = forms.CharField(
        label='Descrição da tag',
        max_length=25,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ex: Ferramentas'
            }
        )
    )

    class Meta:
        model = TagModel
        fields = ['descricao']