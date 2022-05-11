from django.contrib.auth import get_user_model
from django.db import models

from core.models import CreatedModel

User = get_user_model()


class Post(models.Model):
    """Класс определяет модель постов."""
    text = models.TextField('Текст',
                            help_text='Введите текст поста'
                            )
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации'
                                    )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='user_info',
                               verbose_name='Автор'
                               )
    group = models.ForeignKey('Group',
                              on_delete=models.SET_NULL,
                              related_name='group_info',
                              verbose_name='Группа',
                              help_text=(
                                  'Группа, к которой '
                                  'будет относиться пост'
                              ),
                              blank=True,
                              null=True
                              )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]


class Group(models.Model):
    """Класс определяет модель групп к постам."""
    title = models.CharField(max_length=200,
                             verbose_name='Название'
                             )
    slug = models.SlugField(max_length=200,
                            unique=True
                            )
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Comment(CreatedModel):
    """Класс определяет модель для комментариев."""
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments'
                             )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments'
                               )
    text = models.TextField(verbose_name='Комментарий',
                            help_text='Введите текст комментария'
                            )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text


class Follow(models.Model):
    """Класс определяет модель для подписок."""
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower'
                             )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='following'
                               )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (models.UniqueConstraint(
            fields=('user', 'author'),
            name='unique_user_author',
        ),)
