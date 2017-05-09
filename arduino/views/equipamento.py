# coding: utf-8
import datetime
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import View

from arduino.models import CategoriaModel
from arduino.models import TagModel
from arduino.views.painel import Painel
from arduino.forms import EquipamentoForm
from arduino.models import EquipamentoModel, ComentarioModel, UtilizacaoModel
from pagination import pagination


class EquipamentoView(LoginRequiredMixin, View):
    login_url = '/login/'
    template = 'cadastro_equipamento.html'

    def get(self, request, id=None, msg=None, cor_msg=None):
        tags_selecionadas = None
        if request.user.is_superuser:
            if id:  # SE EXISTE ID --> MODO EDIÇÃO
                equipamento = EquipamentoModel.objects.get(pk=id)
                tags_selecionadas = TagModel.objects.filter(equipamento=equipamento)
                form = EquipamentoForm(instance=equipamento)
            else:  # SE NÃO EXISTE ID --> MODO CADASTRO
                form = EquipamentoForm()
        else:
            msg = "Sem permissões de acesso!"
            cor_msg = 'yellow'
            return Painel(request, msg, cor_msg)
        return render(request, self.template, {'form': form, 'id': id, 'msg': msg, 'cor_msg': cor_msg,
                                               'tags': TagModel.objects.all(), 'tags_selecionadas': tags_selecionadas})

    def post(self, request, id=None, msg=None, cor_msg=None):
        if request.user.is_superuser:
            global qtd_total_banco
            tags_selecionadas = None
            if id:  # EDIÇÃO
                id = request.POST['id']
                equipamento_banco = EquipamentoModel.objects.get(pk=id)
                qtd_total_banco = equipamento_banco.quantidade_total
                form = EquipamentoForm(instance=equipamento_banco, data=request.POST)
            else:  # CADASTRO NOVO
                form = EquipamentoForm(data=request.POST)

            if form.is_valid():
                equipamento = form.save(commit=False)

                if 'foto' in request.FILES:
                    equipamento.foto = request.FILES['foto']

                if not id:
                    equipamento.quantidade_disponivel = equipamento.quantidade_total

                if id:
                    equipamento.quantidade_total = qtd_total_banco

                equipamento.save()
                equipamento.data_registro = datetime.datetime.now()
                equipamento.save()

                for tag in TagModel.objects.all():
                    tag = TagModel.objects.get(pk=tag.id)
                    tag.equipamento.remove(equipamento)

                for id_tag in request.POST.getlist('tags'):
                    tag = TagModel.objects.get(pk=id_tag)
                    tag.equipamento.add(equipamento)

                if id:
                    msg = "Alterações efetuadas com sucesso!"
                else:
                    msg = "Equipamento cadastrado com sucesso!"
                cor_msg = "green"
                tags_selecionadas = TagModel.objects.filter(equipamento=equipamento)
            else:
                print(form.errors)
                msg = "Formulário inválido! Tente novamente"
                cor_msg = "red"
            return render(request, self.template, {'form': form, 'id': id, 'msg': msg, 'cor_msg': cor_msg,
                                                   'tags_selecionadas': tags_selecionadas,
                                                   'tags': TagModel.objects.all()})
        else:
            msg = "Sem permissões de acesso!"
            cor_msg = 'yellow'
            return Painel(request, msg, cor_msg)

    @classmethod
    @method_decorator(login_required)
    def ExcluirEquipamento(self, request, id=None):
        if request.user.is_superuser:
            if id:
                equipamento = EquipamentoModel.objects.get(pk=id)
                if equipamento:
                    equipamento = EquipamentoModel.objects.get(id=id)
                    equipamento.foto.delete()
                    equipamento.delete()
                    msg = "Equipamento excluído com sucesso."
                    cor_msg = "green"
                else:
                    msg = "Não foi possível encontrar o equipamento."
                    cor_msg = 'red'
            else:
                msg = "Não foi possível encontrar o equipamento."
                cor_msg = 'red'
        else:
            msg = "Sem permissões de acesso!"
            cor_msg = 'yellow'
        return Painel(request, msg, cor_msg)

    @classmethod
    @method_decorator(login_required)
    def VisualizarEquipamento(self, request, id=None, msg=None, cor_msg=None):
        context_dict = {}
        try:
            equipamento = EquipamentoModel.objects.get(pk=id)
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
        context_dict['usuarios'] = User.objects.all()
        context_dict['msg'] = msg
        context_dict['cor_msg'] = cor_msg
        context_dict['tags'] = TagModel.objects.filter(equipamento=id)
        return render(request, 'visualizar_equipamento.html', context_dict)

    @classmethod
    @method_decorator(login_required)
    def AtivarDesativarEquipamento(self, request, id=None):
        if request.user.is_superuser:
            if id:
                equipamento = EquipamentoModel.objects.get(pk=id)
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
        else:
            msg = "Sem permissões de acesso!"
            cor_msg = 'yellow'
        return Painel(request, msg, cor_msg)

    @classmethod
    @method_decorator(login_required)
    def AcrescentarUnidade(self, request, id=None):
        if request.user.is_superuser:
            equipamento = EquipamentoModel.objects.get(id=id)
            equipamento.quantidade_total = str(int(equipamento.quantidade_total) + 1)
            equipamento.quantidade_disponivel = str(int(equipamento.quantidade_disponivel) + 1)
            equipamento.save()
            return EquipamentoView.VisualizarEquipamento(request, id)
        else:
            msg = "Sem permissões de acesso!"
            cor_msg = 'yellow'
            return Painel(request, msg, cor_msg)

    @classmethod
    @method_decorator(login_required)
    def ReduzirUnidade(self, request, id=None, msg=None, cor_msg=None):
        if request.user.is_superuser:
            equipamento = EquipamentoModel.objects.get(id=id)
            if int(equipamento.quantidade_disponivel) > 0 and int(equipamento.quantidade_total > 0):
                equipamento.quantidade_total = str(int(equipamento.quantidade_total) - 1)
                equipamento.quantidade_disponivel = str(int(equipamento.quantidade_disponivel) - 1)
                equipamento.save()
            else:
                msg = "Não existem mais unidades."
                cor_msg = "red"
            return EquipamentoView.VisualizarEquipamento(request, id, msg, cor_msg)
        else:
            msg = "Sem permissões de acesso!"
            cor_msg = 'yellow'
            return Painel(request, msg, cor_msg)

    @classmethod
    @method_decorator(login_required)
    def ListaEquipamentos(self, request, msg=None, cor_msg=None):
        context_dict = {}
        categoria = None
        filtro = None
        tag = None

        if request.GET:
            if 'tag' in request.GET and request.GET['tag'] != "":
                tag = request.GET['tag']
                equipamentos = EquipamentoModel.objects.filter(ativo=True, tagmodel__descricao=tag).order_by('-data_registro')
            else:
                if 'categoria' in request.GET and request.GET['categoria'] != "":
                    categoria = request.GET['categoria']
                    if 'filtro' in request.GET and request.GET['filtro'] != "":
                        filtro = request.GET['filtro']
                        equipamentos = EquipamentoModel.objects.filter(descricao__contains=filtro,
                                                                       ativo=True,
                                                                       categoria=categoria).order_by('-data_registro')
                    else:
                        equipamentos = EquipamentoModel.objects.filter(ativo=True, categoria=categoria).order_by(
                            '-data_registro')
                else:
                    if 'filtro' in request.GET and request.GET['filtro'] != "":
                        filtro = request.GET['filtro']
                        equipamentos = EquipamentoModel.objects.filter(descricao__contains=filtro,
                                                                       ativo=True,).order_by('-data_registro')
                    else:
                        equipamentos = EquipamentoModel.objects.filter(ativo=True).order_by(
                            '-data_registro')
        else:
            equipamentos = EquipamentoModel.objects.filter(ativo=True).order_by('-data_registro')

        for equipamento in equipamentos:
            equipamento.tags = TagModel.objects.filter(equipamento=equipamento.id)

        # PAGINATION
        equipamentos, page_range, ultima = pagination(equipamentos, request.GET.get('page'))
        context_dict['dados'] = equipamentos
        context_dict['page_range'] = page_range
        context_dict['ultima'] = ultima

        context_dict['categorias'] = CategoriaModel.objects.all()
        context_dict['filtro'] = filtro
        context_dict['categoria'] = categoria
        context_dict['tag'] = tag
        context_dict['msg'] = msg
        context_dict['cor_msg'] = cor_msg
        return render(request, 'lista_equipamentos.html', context_dict)

    @classmethod
    @method_decorator(login_required)
    def ListaEquipamentosDesativados(self, request, msg=None, cor_msg=None):
        context_dict = {}
        equipamentos = EquipamentoModel.objects.filter(ativo=False).order_by('-data_registro')
        for equipamento in equipamentos:
            equipamento.tags = TagModel.objects.filter(equipamento=equipamento.id)

        # PAGINATION
        equipamentos, page_range, ultima = pagination(equipamentos, request.GET.get('page'))
        context_dict['dados'] = equipamentos
        context_dict['page_range'] = page_range
        context_dict['ultima'] = ultima

        context_dict['dados'] = equipamentos
        context_dict['msg'] = msg
        context_dict['cor_msg'] = cor_msg
        return render(request, 'lista_equipamentos_desativados.html', context_dict)

    @classmethod
    @method_decorator(login_required)
    def ListaMeusEmprestimos(self, request, msg=None, cor_msg=None):
        context_dict = {}
        emprestimos = UtilizacaoModel.objects.filter(usuario__exact=request.user, ativo=True)

        for emprestimo in emprestimos:
            emprestimo.equipamento.tags = TagModel.objects.filter(equipamento=emprestimo.equipamento.id)

        # PAGINATION
        equipamentos, page_range, ultima = pagination(emprestimos, request.GET.get('page'))
        context_dict['dados'] = equipamentos
        context_dict['page_range'] = page_range
        context_dict['ultima'] = ultima

        context_dict['dados'] = equipamentos
        context_dict['msg'] = msg
        context_dict['cor_msg'] = cor_msg
        return render(request, 'lista_meus_emprestimos.html', context_dict)

    @classmethod
    @method_decorator(login_required)
    def Comentar(self, request, id=None):
        usuario = request.user
        equipamento = EquipamentoModel.objects.get(pk=id)
        mensagem = request.POST['mensagem']

        comentario = ComentarioModel(
            usuario=usuario,
            equipamento=equipamento,
            mensagem=mensagem
        )
        comentario.save()

        return EquipamentoView.VisualizarEquipamento(request, id)

    @classmethod
    @method_decorator(login_required)
    def Emprestar(self, request, id=None):
        if request.user.is_superuser:
            equipamento = EquipamentoModel.objects.get(pk=id)
            usuario = User.objects.get(pk=request.POST['usuario'])
            qtd_a_emprestar = int(request.POST['quantidade'])
            qtd_disponivel = int(equipamento.quantidade_disponivel)
            if qtd_disponivel >= qtd_a_emprestar > 0:
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
            return EquipamentoView.VisualizarEquipamento(request, id, msg, cor_msg)
        else:
            msg = "Sem permissões de acesso!"
            cor_msg = 'yellow'
            return Painel(request, msg, cor_msg)

    @classmethod
    @method_decorator(login_required)
    def Devolver(self, request, id_utilizacao=None):
        if request.user.is_superuser:
            utilizacao = UtilizacaoModel.objects.get(pk=id_utilizacao)
            id_equipamento = utilizacao.equipamento.id

            equipamento = utilizacao.equipamento
            equipamento.quantidade_disponivel = str(
                int(equipamento.quantidade_disponivel) + int(utilizacao.quantidade_utilizada))
            equipamento.save()
            utilizacao.ativo = False
            utilizacao.save()

            msg = "Devolvido com sucesso."
            cor_msg = "green"
            return EquipamentoView.VisualizarEquipamento(request, id_equipamento, msg, cor_msg)
        else:
            msg = "Sem permissões de acesso!"
            cor_msg = 'yellow'
            return Painel(request, msg, cor_msg)
