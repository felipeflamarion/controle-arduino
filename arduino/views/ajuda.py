# coding: utf-8
from django.shortcuts import render


def Ajuda(request):
    return render(request, 'ajuda.html')
