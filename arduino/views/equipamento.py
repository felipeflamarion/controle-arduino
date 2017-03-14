# coding:utf-8
from django.shortcuts import render, HttpResponseRedirect
from django.core import urlresolvers
from django.views.generic import View
from arduino.forms import EquipamentoForm


class CadastroEquipamento(View):

    template = 'cadastro_equipamento.html'

    def get(self, request):
        context = {}
        context['equipamento_form'] = EquipamentoForm()
        return render(request, self.template, context)

    def post(self, request):
        context = {}
        equipamento_form = EquipamentoForm(data=request.POST)

        if equipamento_form.is_valid():
            equipamento = equipamento_form.save(commit=False)

            if 'foto' in request.FILES:
                equipamento.foto = request.FILES['foto']
                equipamento.save()
                return HttpResponseRedirect(urlresolvers.reverse('painel'))
            else:
                print('Error: Image upload have been failed!')
        else:
            print('Error: The form was submited with errors!')

        context['usuario_form'] = equipamento_form
        return render(request, self.template, context)
