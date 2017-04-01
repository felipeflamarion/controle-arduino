from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def pagination(request, dados):
    paginator = Paginator(dados, 10)
    page = request.GET.get('page')
    try:
        dados = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        dados = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        dados = paginator.page(paginator.num_pages)

    return dados
