# api/urls.py


# ver1
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from recipes.views import RecipeViewSet, TagViewSet, IngredientViewSet
from users.views import UserViewSet


router = DefaultRouter()
router.register('users', UserViewSet)
router.register('recipes', RecipeViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'auth/', include('djoser.urls.authtoken')),
]


# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import (
#     TagViewSet,
#     IngredientViewSet,
#     RecipeViewSet,
#     FavoriteViewSet,
#     ShoppingCartViewSet,
# )
# from users.views import SubscriptionsViewSet, SubscribeAddDelView

# from django.urls import include, path
# from rest_framework.routers import DefaultRouter

# from api.views import (
#     FavoriteViewSet,
#     IngredientViewSet,
#     RecipeViewSet,
#     ShoppingCartViewSet,
#     TagViewSet
# )
# from users.views import SubscribeAddDelView, SubscriptionsViewSet

# app_name = 'api'

# router_v1 = DefaultRouter()

# router_v1.register('recipes', RecipeViewSet, basename='recipes')
# router_v1.register(
#     r'recipes/(?P<recipe_id>\d+)/favorite',
#     FavoriteViewSet,
#     basename='favorite'
# )
# router_v1.register(
#     'users/subscriptions',
#     SubscriptionsViewSet,
#     basename='subscriptions'
# )
# router_v1.register('tags', TagViewSet, basename='tags')
# router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
# router_v1.register(
#     r'recipes/(?P<recipe_id>\d+)/shopping_cart',
#     ShoppingCartViewSet,
#     basename='shopping_cart'
# )

# urlpatterns = [
#     path(
#         'recipes/download_shopping_cart/',
#         ShoppingCartViewSet.as_view({'get': 'download_shopping_cart'})
#     ),
#     path('', include(router_v1.urls)),
#     path('auth/', include('djoser.urls')),
#     path('auth/', include('djoser.urls.authtoken')),
#     path('users/', include('users.urls')),
#     path('users/<int:user_id>/subscribe/', SubscribeAddDelView.as_view()),
# ]


# router = DefaultRouter()
# router.register(r'tags', TagViewSet, basename='tags')
# router.register(r'ingredients', IngredientViewSet, basename='ingredients')
# router.register(r'recipes', RecipeViewSet, basename='recipes')
# router.register(r'favorites', FavoriteViewSet, basename='favorites')
# router.register(r'shopping_cart', ShoppingCartViewSet, basename='shopping-cart')
# router.register(r'subscriptions', SubscriptionsViewSet, basename='subscriptions')

# urlpatterns = [
#     path('', include(router.urls)),
#     path('subscribe/<int:user_id>/', SubscribeAddDelView.as_view(), name='subscribe-add-del'),
# ]
