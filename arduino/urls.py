# coding: utf-8
from django.conf.urls import url
from django.views.generic import TemplateView
from arduino import views
from views import *


urlpatterns = [
    # PRINCIPAL
    url(r'^$', views.Inicio),
    url(r'^inicio/$', views.Inicio, name='inicio'),
    url(r'^ajuda/$', TemplateView.as_view(template_name='ajuda.html'), name='ajuda'),

    # USUÁRIO
    url(r'^cadastro/$', CadastroUsuarioView.as_view(), name='cadastro_usuario'),
    url(r'^login/$', views.Login, name='login'),
    url(r'^logout/$', views.Logout, name='logout'),

    # PÁGINAS
    url(r'^painel/$', views.Painel, name='painel'),
    url(r'^lista/equipamentos$', views.ListaEquipamentos, name='lista_equipamentos'),
    url(r'^lista/equipamentos/desativados$', views.ListaEquipamentosDesativados, name='lista_equipamentos_desativados'),

    url(r'^equipamento/(?P<id_equipamento>[\d]+)/$', VisualizarEquipamento,
        name='visualizar_equipamento'),
    url(r'^equipamento/cadastrar/$', EquipamentoView.as_view(), name='cadastro_equipamento'),
    url(r'^equipamento/editar/(?P<id_equipamento>\d+)/$', EquipamentoView.as_view(), name='editar_equipamento'),
    url(r'^equipamento/excluir/(?P<id_equipamento>[\d]+)/$', ExcluirEquipamento,
        name='excluir_equipamento'),
    url(r'^equipamento/ativar_desativar/(?P<id_equipamento>[\d]+)/$', AtivarDesativarEquipamento,
        name='ativar_desativar_equipamento'),
    url(r'^equipamento/acrescentar/(?P<id_equipamento>[\d]+)/$', AcrescentarUnidade,
        name='acrescentar_equipamento'),
    url(r'^equipamento/reduzir/(?P<id_equipamento>[\d]+)/$', ReduzirUnidade, name='reduzir_equipamento'),
    url(r'^equipamento/comentar/(?P<id_equipamento>[\d]+)/$', views.Comentar, name='comentar'),
    url(r'^equipamento/emprestar/(?P<id_equipamento>[\d]+)/$', views.Emprestar, name='emprestar'),
    url(r'^equipamento/devolver/(?P<id_utilizacao>[\d]+)/$', views.Devolver, name='devolver'),

    # 404
    # url(r'', TemplateView.as_view(template_name='404.html'), name='404'),
]
