# coding: utf-8
from django.shortcuts import render, HttpResponseRedirect
from django.core import urlresolvers
from django.views.generic import View
from arduino.forms import EquipamentoForm
from arduino.models import EquipamentoModel, ComentarioModel, UtilizacaoModel


class CadastroEquipamentoView(View):
    template = 'cadastro_equipamento.html'

    def get(self, request):
        context_dict = {'equipamento_form': EquipamentoForm()}
        return render(request, self.template, context_dict)

    def post(self, request):
        context_dict = {}
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

        context_dict['usuario_form'] = equipamento_form
        return render(request, self.template, context_dict)


class VisualizarEquipamentoView(View):
    template = 'visualizar_equipamento.html'

    def get(self, request, id_equipamento=None):
        context_dict = {}
        try:
            equipamento = EquipamentoModel.objects.get(id=id_equipamento)
            comentarios = ComentarioModel.objects.filter(equipamento=equipamento).order_by('data')
            utilizacoes = UtilizacaoModel.objects.filter(equipamento=equipamento, ativo=True).order_by('quantidade_utilizada')

            context_dict['comentarios'] = comentarios
            context_dict['equipamento'] = equipamento
            context_dict['utilizacoes'] = utilizacoes

            return render(request, self.template, context_dict)
        except:
            pass
        return HttpResponseRedirect(urlresolvers.reverse('painel'))


class DesativarEquipamentoView(View):

    def get(self, request, id_equipamento=None):
        try:
            equipamento = EquipamentoModel.objects.get(id=id_equipamento)
            equipamento.ativo = False
            equipamento.save()
            return HttpResponseRedirect(urlresolvers.reverse('visualizar_equipamento', args=[equipamento.id]))
        except:
            print("Houveram durante a desativação do equipamento!")
            return HttpResponseRedirect(urlresolvers.reverse('painel'))


class AtivarEquipamentoView(View):

    def get(self, request, id_equipamento=None):
        try:
            equipamento = EquipamentoModel.objects.get(id=id_equipamento)
            equipamento.ativo = True
            equipamento.save()
            return HttpResponseRedirect(urlresolvers.reverse('visualizar_equipamento', args=[equipamento.id]))
        except:
            print("Houveram durante a ativação do equipamento")
            return HttpResponseRedirect(urlresolvers.reverse('painel'))


class AcrescentarUnidadeView(View):

    def get(self, request, id_equipamento=None):
        try:
            equipamento = EquipamentoModel.objects.get(id=id_equipamento)
            equipamento.quantidade_total = str(int(equipamento.quantidade_total) + 1)
            equipamento.quantidade_disponivel = str(int(equipamento.quantidade_disponivel) + 1)
            equipamento.save()
        except:
            print("Houveram erros ao acrescentar unidade")
        return HttpResponseRedirect(urlresolvers.reverse('visualizar_equipamento', args=[id_equipamento]))


class ReduzirUnidadeView(View):

    def get(self, request, id_equipamento=None):
        try:
            equipamento = EquipamentoModel.objects.get(id=id_equipamento)
            if int(equipamento.quantidade_disponivel) > 0:
                equipamento.quantidade_total = str(int(equipamento.quantidade_total) - 1)
                equipamento.quantidade_disponivel = str(int(equipamento.quantidade_disponivel) - 1)
                equipamento.save()
        except:
            print("Houveram erros ao reduzir unidade")
        return HttpResponseRedirect(urlresolvers.reverse('visualizar_equipamento', args=[id_equipamento]))
