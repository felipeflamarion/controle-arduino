# coding: utf-8
from django.shortcuts import render, HttpResponseRedirect
from django.core import urlresolvers
from django.views.generic import View
from arduino.views.painel import Painel
from arduino.forms import EquipamentoForm
from arduino.models import EquipamentoModel, ComentarioModel, UtilizacaoModel


class CadastroEquipamentoView(View):
    template = 'cadastro_equipamento.html'

    def get(self, request, id_equipamento=None):
        if id_equipamento:  # SE EXISTE ID --> MODO EDIÇÃO
            equipamento = EquipamentoModel.objects.get(pk=id_equipamento)
            form = EquipamentoForm(instance=equipamento, )
        else:  # SE NÃO EXISTE ID --> MODO CADASTRO
            form = EquipamentoForm()
        return render(request, self.template, {'form': form, 'id': id_equipamento})

    def post(self, request, id_equipamento=None):
        msg = ""
        cor_msg = ""
        global qtd_total_banco
        if id_equipamento:  # EDIÇÃO
            id_equipamento = request.POST['id']
            equipamento_banco = EquipamentoModel.objects.get(pk=id_equipamento)
            qtd_total_banco = equipamento_banco.quantidade_total
            form = EquipamentoForm(instance=equipamento_banco, data=request.POST)
        else:  # CADASTRO NOVO
            form = EquipamentoForm(data=request.POST)

        if form.is_valid():
            equipamento = form.save(commit=False)

            if 'foto' in request.FILES:
                equipamento.foto = request.FILES['foto']

            if not id_equipamento:
                equipamento.quantidade_disponivel = equipamento.quantidade_total

            if id_equipamento:
                equipamento.quantidade_total = qtd_total_banco

            equipamento.save()

            if id_equipamento:
                msg = "Alterações efetuadas com sucesso!"
            else:
                msg = "Equipamento cadastrado com sucesso!"
            cor_msg = "green"
            form = EquipamentoForm()
        else:
            print(form.errors)
            msg = "Formulário inválido! Tente novamente"
            cor_msg = "red"
        return render(request, self.template, {'form': form, 'id': id_equipamento, 'msg': msg, 'cor_msg': cor_msg})


class ExcluirEquipamentoView(View):
    def get(self, request, id_equipamento=None):
        try:
            equipamento = EquipamentoModel.objects.get(id=id_equipamento)
            equipamento.delete()
            msg = "Equipamento excluído com sucesso."
            cor_msg = "green"
        except:
            print("Houveram erros durante a exclusão do equipamento!")
            msg = "Erro ao excluir o equipamento."
            cor_msg = "red"
        return Painel(request, msg, cor_msg)


class VisualizarEquipamentoView(View):
    template = 'visualizar_equipamento.html'

    def get(self, request, id_equipamento=None):
        context_dict = {}
        try:
            equipamento = EquipamentoModel.objects.get(id=id_equipamento)
            comentarios = ComentarioModel.objects.filter(equipamento=equipamento).order_by('data')
            utilizacoes = UtilizacaoModel.objects.filter(equipamento=equipamento, ativo=True).order_by(
                'quantidade_utilizada')

            context_dict['comentarios'] = comentarios
            context_dict['equipamento'] = equipamento
            context_dict['utilizacoes'] = utilizacoes

            return render(request, self.template, context_dict)
        except:
            pass
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
