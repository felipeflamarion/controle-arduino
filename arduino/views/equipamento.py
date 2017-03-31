# coding: utf-8
from django.shortcuts import render
from django.views.generic import View
from arduino.views.painel import Painel
from arduino.forms import EquipamentoForm
from arduino.models import EquipamentoModel, ComentarioModel, UtilizacaoModel
from django.shortcuts import HttpResponseRedirect
from django.core import urlresolvers


class EquipamentoView(View):
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

    @classmethod
    def ExcluirEquipamento(self, request, id_equipamento=None, msg=None, cor_msg=None):
        if id_equipamento:
            equipamento = EquipamentoModel.objects.get(pk=id_equipamento)
            if equipamento:
                equipamento = EquipamentoModel.objects.get(id=id_equipamento)
                equipamento.foto.delete()
                equipamento.delete()
                msg = "Equipamento excluído com sucesso."
                cor_msg = "green"
                return Painel(request, msg, cor_msg)
        msg = "Não foi possível encontrar o equipamento."
        cor_msg = 'red'
        return Painel(request, msg, cor_msg)

    @classmethod
    def VisualizarEquipamento(self, request, id_equipamento=None, msg=None, cor_msg=None):
        context_dict = {}
        try:
            equipamento = EquipamentoModel.objects.get(pk=id_equipamento)
        except EquipamentoModel.DoesNotExist:
            msg = "Não existe equipamento com esse ID!"
            cor_msg = "red"
            return Painel(request, msg, cor_msg)
        comentarios = ComentarioModel.objects.filter(equipamento=equipamento).order_by('data')
        utilizacoes = UtilizacaoModel.objects.filter(equipamento=equipamento, ativo=True).order_by(
            'quantidade_utilizada')
        if utilizacoes.count() >= 1:
            context_dict['ultimo'] = utilizacoes[utilizacoes.count() - 1]
        else:
            context_dict['ultimo'] = None
        context_dict['comentarios'] = comentarios
        context_dict['equipamento'] = equipamento
        context_dict['utilizacoes'] = utilizacoes
        return render(request, 'visualizar_equipamento.html', context_dict)

    @classmethod
    def AtivarDesativarEquipamento(self, request, id_equipamento=None):
        if id_equipamento:
            equipamento = EquipamentoModel.objects.get(pk=id_equipamento)
            if equipamento:
                if equipamento.ativo:
                    equipamento.ativo = False
                    equipamento.save()
                    msg = "Equipamento desativado com sucesso."
                    cor_msg = 'green'
                    return EquipamentoView.VisualizarEquipamento(request, equipamento.id, msg, cor_msg)
                else:
                    equipamento.ativo = True
                    equipamento.save()
                    msg = "Equipamento ativado com sucesso."
                    cor_msg = 'green'
                    return EquipamentoView.VisualizarEquipamento(request, equipamento.id, msg, cor_msg)
        msg = "Não foi possível encontrar o equipamento."
        cor_msg = 'red'
        return Painel(request, msg, cor_msg)

    @classmethod
    def AcrescentarUnidade(self, request, id_equipamento=None):
        equipamento = EquipamentoModel.objects.get(id=id_equipamento)
        equipamento.quantidade_total = str(int(equipamento.quantidade_total) + 1)
        equipamento.quantidade_disponivel = str(int(equipamento.quantidade_disponivel) + 1)
        equipamento.save()
        return EquipamentoView.VisualizarEquipamento(request, id_equipamento)

    @classmethod
    def ReduzirUnidade(self, request, id_equipamento=None):
        equipamento = EquipamentoModel.objects.get(id=id_equipamento)
        if int(equipamento.quantidade_disponivel) > 0 and int(equipamento.quantidade_total > 0):
            equipamento.quantidade_total = str(int(equipamento.quantidade_total) - 1)
            equipamento.quantidade_disponivel = str(int(equipamento.quantidade_disponivel) - 1)
            equipamento.save()
            return EquipamentoView.VisualizarEquipamento(request, id_equipamento)
        else:
            return EquipamentoView.VisualizarEquipamento(request, id_equipamento, msg="Não existem mais unidades.", cor_msg="red")

    @classmethod
    def ListaEquipamentos(self, request, msg=None, cor_msg=None):
        context_dict = {}
        context_dict['equipamentos'] = EquipamentoModel.objects.filter(ativo=True)
        context_dict['msg'] = msg
        context_dict['cor_msg'] = cor_msg
        return render(request, 'lista_equipamentos.html', context_dict)

    @classmethod
    def ListaEquipamentosDesativados(self, request, msg=None, cor_msg=None):
        context_dict = {}
        context_dict['equipamentos'] = EquipamentoModel.objects.filter(ativo=False)
        context_dict['msg'] = msg
        context_dict['cor_msg'] = cor_msg
        return render(request, 'lista_equipamentos_desativados.html', context_dict)

    @classmethod
    def Comentar(self, request, id_equipamento=None):
        usuario = request.user
        equipamento = EquipamentoModel.objects.get(pk=id_equipamento)
        mensagem = request.POST['mensagem']

        comentario = ComentarioModel(
            usuario=usuario,
            equipamento=equipamento,
            mensagem=mensagem
        )
        comentario.save()

        return HttpResponseRedirect(urlresolvers.reverse('visualizar_equipamento', args=[id_equipamento]))

    @classmethod
    def Emprestar(self, request, id_equipamento):
        equipamento = EquipamentoModel.objects.get(pk=id_equipamento)
        usuario = request.user
        qtd_a_emprestar = int(request.POST.get('quantidade'))
        qtd_disponivel = int(equipamento.quantidade_disponivel)
        if qtd_a_emprestar <= qtd_disponivel and qtd_a_emprestar > 0:
            utilizacao = UtilizacaoModel(
                equipamento=equipamento,
                usuario=usuario,
                quantidade_utilizada=qtd_a_emprestar
            )

            equipamento.quantidade_disponivel = qtd_disponivel - qtd_a_emprestar
            equipamento.save()
            utilizacao.save()
            msg = "Empréstimo realizado com sucesso."
            cor_msg = "green"
        else:
            msg = "Quantidade inválida."
            cor_msg = "red"

        return EquipamentoView.VisualizarEquipamento(request, id_equipamento, msg=msg, cor_msg=cor_msg)

    @classmethod
    def Devolver(self, request, id_utilizacao):
        utilizacao = UtilizacaoModel.objects.get(pk=id_utilizacao)
        id_equipamento = utilizacao.equipamento.id

        if request.user == utilizacao.usuario:
            equipamento = utilizacao.equipamento
            equipamento.quantidade_disponivel = str(
                int(equipamento.quantidade_disponivel) + int(utilizacao.quantidade_utilizada))
            equipamento.save()
            utilizacao.ativo = False
            utilizacao.save()
        return EquipamentoView.VisualizarEquipamento(request, id_equipamento)
