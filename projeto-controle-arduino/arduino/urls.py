#coding: utf-8
from django.conf.urls import url

from views import *

urlpatterns = [
    url(r'^$', InicioView.as_view(), name='inicio'),
    url(r'^inicio/$', InicioView.as_view(), name='inicio'),
    url(r'^index/$', InicioView.as_view(), name='inicio'),

    url(r'^cadastro/$', CadastroUsuario.as_view(), name='cadastro_usuario')
]