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

    url(r'^painel/$', views.Painel, name='painel'),

    url(r'^equipamento/(?P<id_equipamento>[\d]+)/$', VisualizarEquipamento,
        name='visualizar_equipamento'),
    url(r'^equipamento/cadastrar/$', CadastroEquipamentoView.as_view(), name='cadastro_equipamento'),
    url(r'^equipamento/editar/(?P<id_equipamento>\d+)/$', CadastroEquipamentoView.as_view(), name='editar_equipamento'),
    url(r'^equipamento/excluir/(?P<id_equipamento>[\d]+)/$', ExcluirEquipamento,
        name='excluir_equipamento'),
    url(r'^equipamento/ativar_desativar/(?P<id_equipamento>[\d]+)/$', AtivarDesativarEquipamento,
        name='ativar_desativar_equipamento'),

    # Terminar
    url(r'^equipamento/acrescentar/(?P<id_equipamento>[\d]+)/$', AcrescentarUnidade,
        name='acrescentar_equipamento'),
    url(r'^equipamento/reduzir/(?P<id_equipamento>[\d]+)/$', ReduzirUnidade, name='reduzir_equipamento'),
    url(r'^equipamento/comentar/(?P<id_equipamento>[\d]+)/$', ComentarView.as_view(), name='comentar'),
    url(r'^equipamento/emprestar/(?P<id_equipamento>[\d]+)/$', EmprestarView.as_view(), name='emprestar'),
    url(r'^equipamento/devolver/(?P<id_utilizacao>[\d]+)/$', DevolverView.as_view(), name='devolver'),
]
