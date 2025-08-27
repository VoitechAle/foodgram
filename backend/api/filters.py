

# ver1
from django_filters import rest_framework as filters
from recipes.models import Recipe

class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug', label='Tags')
    author = filters.CharFilter(field_name='author__username', lookup_expr='iexact', label='Author')
    is_favorited = filters.BooleanFilter(method='filter_favorited')
    is_in_shopping_cart = filters.BooleanFilter(method='filter_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']

    def filter_favorited(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(favorited_by__recipe_subscriber=user)
        return queryset

    def filter_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(shopping_cart__cart_owner=user)
        return queryset
