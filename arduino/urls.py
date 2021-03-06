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
    url(r'^lista/equipamentos/$', EquipamentoView.ListaEquipamentos, name='lista_equipamentos'),
    url(r'^lista/equipamentos/desativados/$', EquipamentoView.ListaEquipamentosDesativados, name='lista_equipamentos_desativados'),
    url(r'^lista/emprestimos/$', EquipamentoView.ListaEmprestimos, name='emprestimos'),
    url(r'^lista/meus_emprestimos/$', EquipamentoView.ListaMeusEmprestimos, name='meus_emprestimos'),

    url(r'^equipamento/(?P<id>[\d]+)/$', EquipamentoView.VisualizarEquipamento,
        name='visualizar_equipamento'),
    url(r'^equipamento/cadastrar/$', EquipamentoView.as_view(), name='cadastro_equipamento'),
    url(r'^equipamento/editar/(?P<id>\d+)/$', EquipamentoView.as_view(), name='editar_equipamento'),
    url(r'^equipamento/excluir/(?P<id>[\d]+)/$', EquipamentoView.ExcluirEquipamento,
        name='excluir_equipamento'),
    url(r'^equipamento/ativar_desativar/(?P<id>[\d]+)/$', EquipamentoView.AtivarDesativarEquipamento,
        name='ativar_desativar_equipamento'),
    url(r'^equipamento/acrescentar/(?P<id>[\d]+)/$', EquipamentoView.AcrescentarUnidade,
        name='acrescentar_equipamento'),
    url(r'^equipamento/reduzir/(?P<id>[\d]+)/$', EquipamentoView.ReduzirUnidade, name='reduzir_equipamento'),
    url(r'^equipamento/comentar/(?P<id>[\d]+)/$', EquipamentoView.Comentar, name='comentar'),
    url(r'^equipamento/emprestar/(?P<id>[\d]+)/$', EquipamentoView.Emprestar, name='emprestar'),
    url(r'^equipamento/devolver/(?P<id_utilizacao>[\d]+)/$', EquipamentoView.Devolver, name='devolver'),

    url(r'^tag/$', TagView.as_view(), name='cadastro_tag'),
    url(r'^tag/editar/(?P<id>[\d]+)/$', TagView.as_view(), name='edita_tag'),
    url(r'^tag/excluir/(?P<id>[\d]+)/$', TagView.ExcluirTag, name='exclui_tag'),

    # 404
    url(r'', TemplateView.as_view(template_name='404.html'), name='404'),
]
