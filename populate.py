import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from arduino.models import CategoriaModel, LocalModel

def populate():
    ferramenta = add_categoria('ferramenta')
    arduino = add_categoria('arduino')
    shield = add_categoria('shield')
    dispositivo = add_categoria('dispositivo')
    cabo = add_categoria('cabo')

    local1 = add_local('Local 1')
    local2 = add_local('Local 2')
    local3 = add_local('Local 3')
    local4 = add_local('Local 4')
    local5 = add_local('Local 5')


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
