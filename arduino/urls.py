#coding: utf-8
from django.conf.urls import url

from views import *

urlpatterns = [
    url(r'^$', InicioView.as_view()),
    url(r'^inicio/$', InicioView.as_view(), name='inicio'),

    url(r'^cadastro/$', CadastroUsuario.as_view(), name='cadastro_usuario'),
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^logout/$', Logout.as_view(), name='logout'),

    url(r'^painel/$', Painel.as_view(), name='painel'),
    url(r'^equipamento/cadastrar/$', CadastroEquipamento.as_view(), name='cadastro_equipamento'),

    url(r'^equipamento/desativar/(?P<id_equipamento>[\d]+)$', DesativarEquipamento.as_view(), name='desativar_equipamento'),
    url(r'^equipamento/ativar/(?P<id_equipamento>[\d]+)$', AtivarEquipamento.as_view(), name='ativar_equipamento'),
    url(r'^equipamento/(?P<id_equipamento>[\d]+)$', VisualizarEquipamento.as_view(), name='visualizar_equipamento'),

    url(r'^equipamento/comentar/(?P<id_equipamento>[\d]+)$', Comentar.as_view(), name='comentar'),
]