# coding: utf-8
from __future__ import print_function
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django

django.setup()

from arduino.models import CategoriaModel, LocalModel, TagModel, EquipamentoModel


def populate():
    ''' Script de população de BD '''

    ''' CATEGORIA (descricao) '''

    ferramenta = add_categoria('Ferramentas')
    arduino = add_categoria('Arduinos')
    shield = add_categoria('Shields')
    dispositivo = add_categoria('Dispositivos')
    cabo = add_categoria('Cabos')
    conectores = add_categoria('Conectores')
    categoria_outros = add_categoria('Outros')

    ''' LOCAIS (descricao, observacao) '''

    caixa_ferramentas = add_local('Caixa de Ferramentas')
    caixa_novos = add_local('Caixa de Novos')
    caixa_usados = add_local('Caixa de Usados')
    caixa_organizadora_1 = add_local('Caixa Organizadora 1')
    caixa_organizadora_2 = add_local('Caixa Organizadora 2')
    caixa_organizadora_3 = add_local('Caixa Organizadora 3')
    caixa_organizadora_4 = add_local('Caixa Organizadora 3')
    local_outros = add_local('Outros')

    ''' EQUIPAMENTOS (descricao, observacao, quantidade_total, quantidade_disponivel, ativo, data_registro, foto, local, categoria) '''

    equipamento_1 = add_equipamento('Arduino UNO', '', 3, 3, True, None, '', caixa_usados, arduino)
    equipamento_2 = add_equipamento('Raspberry Pi 3 Model B', '', 2, 2, True, None, '', caixa_novos, arduino)
    equipamento_3 = add_equipamento('DHT 22', '', 5, 5, True, None, '', caixa_novos, shield)
    equipamento_4 = add_equipamento('Resistor 10K', '', 40, 40, True, None, '', caixa_organizadora_1, conectores)
    equipamento_5 = add_equipamento('Multímetro', '', 1, 1, True, None, '', caixa_ferramentas, ferramenta)
    equipamento_6 = add_equipamento('Estação de Solda', '', 1, 1, True, None, '', caixa_ferramentas, ferramenta)
    equipamento_7 = add_equipamento('Cabo USB A/B', '', 1, 1, True, None, '', local_outros, cabo)

    ''' TAGS '''

    # tag_resistor = add_tag('resistor', equipamento_4)
    # tag_sensor = add_tag('sensor', equipamento_3)
    # tag_placa = add_tag('placa', equipamento_1)
    # tag_eletricidade = add_tag('eletricidade', equipamento_5)
    # tag_wifi = add_tag('wifi', equipamento_2)
    # tag_bluetooth = add_tag('bluetooth', equipamento_2)
    # tag_ferramenta = add_tag('ferramenta', equipamento_6)
    # tag_cabo = add_tag('cabo', equipamento_7)


def add_categoria(descricao):
    return CategoriaModel.objects.get_or_create(descricao=descricao)[0]


def add_local(descricao, observacao=''):
    return LocalModel.objects.get_or_create(descricao=descricao, observacao=observacao)[0]


def add_equipamento(descricao, observacao, quantidade_total, quantidade_disponivel, ativo, data_registro, foto, local,
                    categoria):
    return EquipamentoModel.objects.get_or_create(descricao=descricao, observacao=observacao,
                                                  quantidade_total=quantidade_total,
                                                  quantidade_disponivel=quantidade_disponivel, ativo=ativo,
                                                  data_registro=data_registro, foto=foto, local=local,
                                                  categoria=categoria)[0]


''' Para popular tags, deve-se popular a tabela associativa também '''
def add_tag(descricao, equipamento):
    return TagModel.objects.get_or_create(descricao=descricao, equipamento=equipamento)[0]



if __name__ == '__main__':
    print("Starting Controle Arduino population script...")
    populate()
