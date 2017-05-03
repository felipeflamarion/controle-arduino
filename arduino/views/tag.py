#coding:utf-8
from django.shortcuts import render
from django.views.generic import View
from arduino.forms import TagForm
from arduino.models import TagModel
import random

class TagView(View):

    template = 'cadastro_tag.html'

    def get(self, request):
        context_dict = {}
        form = TagForm()
        context_dict['form'] = form
        context_dict['tags'] = self.colorizar_tags(TagModel.objects.all().order_by('-id'))
        return render(request, self.template, context_dict)

    def post(self, request):
        context_dict = {}
        form = TagForm(data=request.POST)

        if form.is_valid():
            form.save()
            context_dict['msg'] = 'Tag cadastrada com sucesso'
            context_dict['cor_msg'] = 'green'

        context_dict['form'] = form
        context_dict['tags'] = self.colorizar_tags(TagModel.objects.all().order_by('-id'))
        return render(request, self.template, context_dict)

    def colorizar_tags(self, tags):
        tags_coloridas = []
        for tag in tags:
            tags_coloridas.append({
                'id': tag.id,
                'descricao': tag.descricao,
                'cor': self.cor_aleatoria()
            })
        print(tags_coloridas)
        return tags_coloridas

    def cor_aleatoria(self):
        cores = [
            'red',
            'orange',
            'yellow',
            'olive',
            'green',
            'teal',
            'blue',
            'violet',
            'purple',
            'pink',
            'brown',
            'grey',
            'black'
        ]
        cor = cores[random.randrange(0,len(cores))]
        return cor