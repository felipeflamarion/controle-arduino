import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from arduino.models import Categoria, Caixa

def populate():

    ferramenta = add_categoria('ferramenta')
    arduino = add_categoria('arduino')
    shield = add_categoria('shield')
    dispositivo = add_categoria('dispositivo')
    cabo = add_categoria('cabo')

    caixa1 = add_caixa('Caixa 1')
    caixa2 = add_caixa('Caixa 2')
    caixa3 = add_caixa('Caixa 3')
    caixa4 = add_caixa('Caixa 4')
    caixa5 = add_caixa('Caixa 5')

def add_categoria(descricao):
    categoria = Categoria.objects.get_or_create(descricao=descricao)[0]
    categoria.save()
    return categoria

def add_caixa(descricao, observacao=''):
    caixa = Caixa.objects.get_or_create(descricao=descricao, observacao=observacao)[0]
    caixa.save()
    return caixa

if __name__ == '__main__':
    print "Starting Controle Arduino population script..."
    populate()
