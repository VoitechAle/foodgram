# recipes/models.py
# ver2
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True,
                            verbose_name='Название тега')
    slug = models.SlugField(unique=True, verbose_name='Уникальный слаг')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True,
                            verbose_name='Название ингредиента')
    measurement_unit = models.CharField(max_length=50,
                                        verbose_name='Единица измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f"{self.name} ({self.measurement_unit})"


class Recipe(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    title = models.CharField(max_length=200, verbose_name='Название рецепта')
    image = models.ImageField(upload_to='recipes/',
                              verbose_name='Изображение рецепта')
    description = models.TextField(verbose_name='Описание рецепта')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient',
                                         verbose_name='Ингредиенты')
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Время приготовления (в минутах)'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    amount = models.FloatField(
        validators=[MinValueValidator(0.1)],
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        unique_together = ('recipe', 'ingredient')

    def __str__(self):
        return f"""{self.ingredient.name}
                - {self.amount} {self.ingredient.measurement_unit}"""


class ShoppingCart(models.Model):
    cart_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Владелец корзины'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт'
    )

    class Meta:
        unique_together = ('cart_owner', 'recipe')
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзина покупок'

    def __str__(self):
        return f"{self.cart_owner.username} - {self.recipe.title}"

# from django.db import models
# from django.contrib.auth import get_user_model
# from django.core.validators import MinValueValidator, MaxValueValidator
# from colorfield.fields import ColorField

# from api.constants import MAX_MODEL_FIELD_LENGTH

# User = get_user_model()


# class Tag(models.Model):
#     """ Модель тегов. """

#     name = models.CharField('Наименование тега',
#                             max_length=MAX_MODEL_FIELD_LENGTH, unique=True)
#     color = ColorField('Цвет тега', max_length=7, unique=True)
#     slug = models.SlugField(
#         'Слаг тега', max_length=MAX_MODEL_FIELD_LENGTH, unique=True)

#     class Meta:
#         verbose_name = 'Тег'
#         verbose_name_plural = 'Теги'
#         ordering = ('name',)

#     def __str__(self):
#         return f'{self.name}'


# class Ingredient(models.Model):
#     """ Модель ингридиентов. """
#     name = models.CharField(
#         'Название ингридиента',
#         max_length=MAX_MODEL_FIELD_LENGTH,
#         db_index=True
#     )

#     measurement_unit = models.CharField(
#         'Единицы измерения',
#         max_length=MAX_MODEL_FIELD_LENGTH
#     )

#     class Meta:
#         verbose_name = 'Ингридиент'
#         verbose_name_plural = 'Ингридиенты'
#         ordering = ('name',)
#         constraints = [
#             models.UniqueConstraint(
#                 fields=('name', 'measurement_unit'),
#                 name='unique_ingredient')
#         ]

#     def __str__(self) -> str:
#         return f'{self.name}, {self.measurement_unit}'


# class Recipe(models.Model):
#     """ Модель рецептов. """
#     author = models.ForeignKey(
#         User, on_delete=models.CASCADE, verbose_name='Автор рецепта')

#     name = models.CharField(
#         'Название рецепта', max_length=MAX_MODEL_FIELD_LENGTH, db_index=True)
#     image = models.ImageField('Изображение блюда', upload_to='media/')
#     text = models.TextField('Описание рецепта')
#     pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

#     tags = models.ManyToManyField(Tag, verbose_name='Тег')

#     ingredients = models.ManyToManyField(
#         Ingredient, verbose_name='Ингридиенты', through='RecipeIngredient')

#     cooking_time = models.PositiveSmallIntegerField(
#         'Время готовки',
#         validators=[
#             MinValueValidator(
#                 1,
#                 'Время готовки должно быть больше 0.'),
#             MaxValueValidator(
#                 32767,
#                 'Проще купить, чем столько готовить.')
#         ])

#     class Meta:
#         verbose_name = 'Рецепт'
#         verbose_name_plural = 'Рецепты'
#         ordering = ('-pub_date',)
#         default_related_name = 'recipe'
#         constraints = [
#             models.UniqueConstraint(
#                 fields=('name', 'author'),
#                 name='unique_recipes')
#         ]

#     def __str__(self) -> str:
#         return self.name


# class RecipeIngredient(models.Model):
#     """ Ингридиенты для использования в рецепте. """
#     recipe = models.ForeignKey(
#         Recipe, on_delete=models.CASCADE,
#         verbose_name='Название рецепта',
#         related_name='recipe_ingredients')
#     ingredient = models.ForeignKey(
#         Ingredient, on_delete=models.CASCADE,
#         verbose_name='Ингредиент рецепта')
#     amount = models.PositiveSmallIntegerField(
#         'Количество ингредиента',
#         validators=[
#             MinValueValidator(
#                 1,
#                 'Количество ингридиента должно быть больше 0.'),
#             MaxValueValidator(
#                 999999,
#                 'Куда тебе столько?')
#         ])

#     class Meta:
#         verbose_name = 'Ингридиент для рецепта'
#         verbose_name_plural = 'Ингридиенты для рецепта'
#         ordering = ('recipe',)

#     def __str__(self) -> str:
#         return f'{self.ingredient} -- {self.amount}'


# class ShoppingCart(models.Model):
#     """ Модель списка покупок. """
#     customer = models.ForeignKey(
#         User,
#         related_name='shoppingcart',
#         verbose_name='Покупатель',
#         on_delete=models.CASCADE)
#     recipe = models.ForeignKey(
#         Recipe,
#         related_name='shoppingcart',
#         verbose_name='Рецепт блюда',
#         on_delete=models.CASCADE)

#     class Meta:
#         verbose_name = 'Список покупок'
#         verbose_name_plural = 'Список покупок'
#         ordering = ('customer',)

#     def __str__(self) -> str:
#         return f'{self.recipe}'


# class Favorite(models.Model):
#     """ Модель избранного. """
#     customer = models.ForeignKey(
#         User,
#         related_name='favorite',
#         verbose_name='Покупатель',
#         on_delete=models.CASCADE)
#     recipe = models.ForeignKey(
#         Recipe,
#         related_name='favorite',
#         verbose_name='Рецепт блюда',
#         on_delete=models.CASCADE)

#     class Meta:
#         verbose_name = 'Любимые рецепты'
#         verbose_name_plural = 'Любимые рецепты'
#         ordering = ('customer',)

#     def __str__(self) -> str:
#         return f'{self.recipe}'


# #ver1
# from django.db import models
# from django.conf import settings
# from django.core.validators import MinValueValidator


# # Create your models here.
# class Tag(models.Model):
#     name = models.CharField(max_length=200, unique=True)
#     slug = models.SlugField(unique=True)

#     def __str__(self):
#         return self.name

# class Ingredient(models.Model):
#     name = models.CharField(max_length=200, unique=True)
#     measurement_unit = models.CharField(max_length=50)

#     def __str__(self):
#         return f"{self.name} ({self.measurement_unit})"

# class Recipe(models.Model):
#     author = models.ForeignKey('users.User', on_delete=models.CASCADE,
#  related_name='recipes')
#     title = models.CharField(max_length=200)
#     image = models.ImageField(upload_to='recipes/')
#     description = models.TextField()
#     ingredients = models.ManyToManyField(Ingredient,
# through='RecipeIngredient')
#     tags = models.ManyToManyField(Tag)
#     cooking_time = models.PositiveIntegerField()

#     def __str__(self):
#         return self.title

# class RecipeIngredient(models.Model):
#     recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
#  related_name='recipe_ingredients')
#     ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
#     amount = models.FloatField()


#     class Meta:
#         unique_together = ('recipe', 'ingredient')

#     def __str__(self):
#         return f"{self.ingredient.name} - {self.amount}
#  {self.ingredient.measurement_unit}"

# class ShoppingCart(models.Model):
#     cart_owner = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='shopping_cart'
#     )
#     recipe = models.ForeignKey(
#         Recipe,
#         on_delete=models.CASCADE,
#         related_name='shopping_cart'
#     )

#     class Meta:
#         unique_together = ('cart_owner', 'recipe')
#         verbose_name = 'Корзина покупок'
#         verbose_name_plural = 'Корзина покупок'

#     def __str__(self):
#         return f"{self.cart_owner.username} - {self.recipe.title}"
