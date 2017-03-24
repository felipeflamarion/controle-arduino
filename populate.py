# coding: utf-8
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django

django.setup()

from arduino.models import CategoriaModel, LocalModel


def populate():
    ferramenta = add_categoria('Ferramentas')
    arduino = add_categoria('Arduinos')
    shield = add_categoria('Shields')
    dispositivo = add_categoria('Dispositivos')
    cabo = add_categoria('Cabos')
    outros = add_categoria('Outros')

    locais = ['Caixa de Ferramentas', 'Caixa de Novos', 'Caixa de Usados', 'Caixa Organizadora 1',
              'Caixa Organizadora 2', 'Caixa Organizadora 3', 'Caixa Organizadora 4']
    for local in locais:
        add_local(local)


def add_categoria(descricao):
    categoria = CategoriaModel.objects.get_or_create(descricao=descricao)[0]
    categoria.save()
    return categoria


def add_local(descricao, observacao=''):
    local = LocalModel.objects.get_or_create(descricao=descricao, observacao=observacao)[0]
    local.save()
    return local


if __name__ == '__main__':
    print "Starting Controle Arduino population script..."
    populate()
