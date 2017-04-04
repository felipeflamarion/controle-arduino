from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def pagination(model, page):
    paginator = Paginator(model, 10)
    limite_paginas_anteriores = 2
    limite_paginas_seguintes = 3
    try:
        dados = paginator.page(page)
    except PageNotAnInteger:
        dados = paginator.page(1)
    except EmptyPage:
        dados = paginator.page(paginator.num_pages)

    # Get the index of the current page
    index = dados.number - 1  # edited to something easier without index
    # This value is maximum index of your pages, so the last page - 1
    max_index = len(paginator.page_range)
    # You want a range of 7, so lets calculate where to slice the list
    start_index = index - limite_paginas_anteriores if index >= limite_paginas_anteriores else 0
    end_index = index + limite_paginas_seguintes if index <= max_index - limite_paginas_seguintes else max_index
    # My new page range

    # page_range = paginator.page_range[start_index:end_index]
    page_range = paginator.page_range
    page_range = list(page_range)
    page_range = page_range[start_index:end_index]

    return dados, page_range, max_index
