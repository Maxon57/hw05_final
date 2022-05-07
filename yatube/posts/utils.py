from django.core.paginator import Paginator


def install_paginator(request, set_records: list):
    """Возвращает обЪект пагинатора."""
    paginator = Paginator(set_records, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
