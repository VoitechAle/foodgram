# recipes/models.py

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Название тега')
    slug = models.SlugField(unique=True, verbose_name='Уникальный слаг')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Название ингредиента')
    measurement_unit = models.CharField(max_length=50, verbose_name='Единица измерения')

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
    image = models.ImageField(upload_to='recipes/', verbose_name='Изображение рецепта')
    description = models.TextField(verbose_name='Описание рецепта')
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', verbose_name='Ингредиенты')
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
        return f"{self.ingredient.name} - {self.amount} {self.ingredient.measurement_unit}"

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
#     author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='recipes')
#     title = models.CharField(max_length=200)
#     image = models.ImageField(upload_to='recipes/')
#     description = models.TextField()
#     ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
#     tags = models.ManyToManyField(Tag)
#     cooking_time = models.PositiveIntegerField()

#     def __str__(self):
#         return self.title

# class RecipeIngredient(models.Model):
#     recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
#     ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
#     amount = models.FloatField()


#     class Meta:
#         unique_together = ('recipe', 'ingredient')

#     def __str__(self):
#         return f"{self.ingredient.name} - {self.amount} {self.ingredient.measurement_unit}"

# class ShoppingCart(models.Model):
#     cart_owner = models.ForeignKey(
#         settings.AUTH_USER_MODEL,  # ссылаемся на кастомную модель пользователя
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