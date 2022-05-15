from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Profile(models.Model):
    """Класс расширяет базовый класс User."""
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='profile'
                                )
    date_birth = models.DateField('Дата рождения',
                                  null=True,
                                  blank=True
                                  )
    photo = models.ImageField('Фото профиля',
                              upload_to='users/',
                              default='users/noname.jpg'
                              )
    location = models.CharField('Место рождения',
                                max_length=200,
                                blank=True
                                )
