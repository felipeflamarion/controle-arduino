# coding: utf-8
from arduino.models import UtilizacaoModel, EquipamentoModel
from arduino.views import VisualizarEquipamento


def Emprestar(request, id_equipamento):
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

    return VisualizarEquipamento(request, id_equipamento, msg=msg, cor_msg=cor_msg)


def Devolver(request, id_utilizacao):
    utilizacao = UtilizacaoModel.objects.get(pk=id_utilizacao)
    id_equipamento = utilizacao.equipamento.id

    if request.user == utilizacao.usuario:
        equipamento = utilizacao.equipamento
        equipamento.quantidade_disponivel = str(
            int(equipamento.quantidade_disponivel) + int(utilizacao.quantidade_utilizada))
        equipamento.save()
        utilizacao.ativo = False
        utilizacao.save()
    return VisualizarEquipamento(request, id_equipamento)