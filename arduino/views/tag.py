# coding: utf-8
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from arduino.forms import TagForm
from arduino.models import TagModel
from arduino.views import Painel


class TagView(LoginRequiredMixin, View):
    login_url = '/login/'
    template = 'cadastro_tag.html'

    def get(self, request, id=None, msg=None, cor_msg=None):
        if request.user.is_superuser:
            context_dict = {}
            if id:  # EDIÇÃO:
                tag = TagModel.objects.get(pk=id)
                form = TagForm(instance=tag)
            else:  # NOVO CADASTRO
                form = TagForm()
            context_dict['id'] = id
            context_dict['form'] = form
            context_dict['tags'] = TagModel.objects.all().order_by('-id')
            context_dict['msg'] = msg
            context_dict['cor_msg'] = cor_msg
            return render(request, self.template, context_dict)
        else:
            msg = "Sem permissões de acesso!"
            cor_msg = 'yellow'
            return Painel(request, msg, cor_msg)

    def post(self, request, id=None, msg=None, cor_msg=None):
        if request.user.is_superuser:
            context_dict = {}
            if id:  # EDIÇÃO
                id = request.POST['id']
                tag_banco = TagModel.objects.get(pk=id)
                form = TagForm(instance=tag_banco, data=request.POST)
            else:  # NOVO CADASTRO
                form = TagForm(data=request.POST)
            if id and tag_banco.descricao == request.POST['descricao']:
                msg = "Defina uma descrição diferente."
                cor_msg = "yellow"
            else:
                if form.is_valid():
                    form.save()

                    if id:
                        msg = "Alterações efetuadas com sucesso!"
                    else:
                        msg = "Tag cadastrada com sucesso!"
                    cor_msg = "green"
                    form = TagForm()
                    id=None
                else:
                    print(form.errors)
                    msg = "Formulário inválido! Tente novamente"
                    cor_msg = "red"

            context_dict['id'] = id
            context_dict['form'] = form
            context_dict['tags'] = TagModel.objects.all().order_by('-id')
            context_dict['msg'] = msg
            context_dict['cor_msg'] = cor_msg
            return render(request, self.template, context_dict)
        else:
            msg = "Sem permissões de acesso!"
            cor_msg = 'yellow'
            return Painel(request, msg, cor_msg)

    @classmethod
    @method_decorator(login_required)
    def ExcluirTag(self, request, id=None):
        context_dict = {}
        if request.user.is_superuser:
            if id:
                tag = TagModel.objects.get(pk=id)
                if tag:
                    tag = TagModel.objects.get(id=id)
                    tag.delete()
                    msg = "Tag excluída com sucesso."
                    cor_msg = "green"
                else:
                    msg = "Não foi possível encontrar a tag."
                    cor_msg = 'red'
            else:
                msg = "Não foi possível encontrar a tag."
                cor_msg = 'red'
        else:
            msg = "Sem permissões de acesso!"
            cor_msg = 'yellow'
        form = TagForm()
        context_dict['form'] = form
        context_dict['tags'] = TagModel.objects.all().order_by('-id')
        context_dict['msg'] = msg
        context_dict['cor_msg'] = cor_msg
        return render(request, self.template, context_dict)
