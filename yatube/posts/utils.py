from django.core.paginator import Paginator
from django.shortcuts import redirect
from posts.models import Follow


def install_paginator(request, set_records: list):
    """Возвращает обЪект пагинатора."""
    paginator = Paginator(set_records, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def check_user(func):
    """Проверка пользователя для подписки."""
    def wrapper(request, *args, **kwargs):
        subscription = Follow.objects.filter(
            user_id=request.user.pk,
            author__username=kwargs['username']
        ).exists()
        if subscription:
            return redirect('posts:profile', kwargs['username'])
        if request.user.username != kwargs['username']:
            return func(request, *args, **kwargs)
        else:
            return redirect('posts:profile', kwargs['username'])
    return wrapper
