# coding: utf-8
from django.conf.urls import url
from arduino import views
from views import *


urlpatterns = [
    url(r'^$', InicioView.as_view()),
    url(r'^inicio/$', InicioView.as_view(), name='inicio'),

    url(r'^cadastro/$', CadastroUsuarioView.as_view(), name='cadastro_usuario'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', views.Logout, name='logout'),

    url(r'^painel/$', PainelView.as_view(), name='painel'),
    url(r'^equipamento/cadastrar/$', CadastroEquipamentoView.as_view(), name='cadastro_equipamento'),

    url(r'^equipamento/desativar/(?P<id_equipamento>[\d]+)$', DesativarEquipamentoView.as_view(),
        name='desativar_equipamento'),
    url(r'^equipamento/ativar/(?P<id_equipamento>[\d]+)$', AtivarEquipamentoView.as_view(), name='ativar_equipamento'),
    url(r'^equipamento/(?P<id_equipamento>[\d]+)$', VisualizarEquipamentoView.as_view(), name='visualizar_equipamento'),
    url(r'^equipamento/acrescentar/(?P<id_equipamento>[\d]+)$', AcrescentarUnidadeView.as_view(),
        name='acrescentar_equipamento'),
    url(r'^equipamento/reduzir/(?P<id_equipamento>[\d]+)$', ReduzirUnidadeView.as_view(), name='reduzir_equipamento'),

    url(r'^equipamento/comentar/(?P<id_equipamento>[\d]+)$', ComentarView.as_view(), name='comentar'),

    url(r'^equipamento/emprestar/(?P<id_equipamento>[\d]+)$', EmprestarView.as_view(), name='emprestar'),
    url(r'^equipamento/devolver/(?P<id_utilizacao>[\d]+)$', DevolverView.as_view(), name='devolver'),
]
