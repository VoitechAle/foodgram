# recipes/admin.py
from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient, ShoppingCart, Tag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'favorites_count', 'cooking_time')
    search_fields = ('title', 'author__username')
    list_filter = ('tags',)

    def favorites_count(self, obj):
        return obj.favorited_by.count()
    favorites_count.short_description = 'Количество добавлений в избранное'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
    list_filter = ('recipe', 'ingredient')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('cart_owner', 'recipe')
    list_filter = ('cart_owner',)

# # ver1
# from django.contrib import admin
# from .models import Recipe, Tag, Ingredient, RecipeIngredient

# @admin.register(Recipe)
# class RecipeAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'favorites_count')
#     search_fields = ('title', 'author__username')
#     list_filter = ('tags',)

#     def favorites_count(self, obj):
#         return obj.favorited_by.count()

# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):
#     list_display = ('name', 'slug')
#     search_fields = ('name',)

# @admin.register(Ingredient)
# class IngredientAdmin(admin.ModelAdmin):
#     list_display = ('name', 'measurement_unit')
#     search_fields = ('name',)
