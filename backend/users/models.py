# users/models.py
# ver1
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

# from recipes.models import Recipe


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='E-mail',
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Логин',
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9]*$',
                message='Введите другой логин!',
            ),
        ]
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
        'password',
    ]

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='follower')  # тот, кто подписывается
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='following')  # на кого подписываются

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_follow')
        ]

    def __str__(self):
        return f"{self.user.username} подписан на {self.author.username}"


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites')
    recipe = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.CASCADE, related_name='favorited_by')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite')
        ]

    def __str__(self):
        return (
            f"{self.user.username} добавил в избранное "
            f"рецепт {self.recipe.title}"
        )

# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.validators import UnicodeUsernameValidator

# from api.constants import (USERNAME_FIELD, REQUIRED_FIELDS,
#                            MAX_USER_MODEL_FIELD_LENGTH)


# class CustomUser(AbstractUser):
#     """ Кастомная модель пользователя. """

#     USERNAME_FIELD = USERNAME_FIELD
#     REQUIRED_FIELDS = REQUIRED_FIELDS

#     username = models.CharField(
#         'Логин',
#         max_length=MAX_USER_MODEL_FIELD_LENGTH,
#         unique=True,
#         validators=[UnicodeUsernameValidator()]
#     )

#     password = models.CharField(
#         'Пароль', max_length=MAX_USER_MODEL_FIELD_LENGTH)

#     email = models.EmailField(
#         'E-mail адрес',
#         unique=True
#     )

#     first_name = models.CharField(
#         'Имя', max_length=MAX_USER_MODEL_FIELD_LENGTH)
#     last_name = models.CharField(
#         'Фамилия', max_length=MAX_USER_MODEL_FIELD_LENGTH)

#     class Meta:
#         verbose_name = 'Пользователь'
#         verbose_name_plural = 'Пользователи'

#     def __str__(self) -> str:
#         return self.username


# class Follow(models.Model):
#     """ Модель подписок. """
#     user = models.ForeignKey(
#         CustomUser,
#         on_delete=models.CASCADE,
#         related_name='follower',
#         verbose_name='Пользователь',
#     )
#     following = models.ForeignKey(
#         CustomUser,
#         on_delete=models.CASCADE,
#         related_name='followings',
#         verbose_name='Подписан'
#     )

#     class Meta:
#         verbose_name = 'Подписчика'
#         verbose_name_plural = 'Подписчики'

#     def __str__(self):
#         return f'{self.user} подписан на {self.following}'
