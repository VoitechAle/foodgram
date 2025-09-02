# api/urls.py

# ver1
from django.urls import include, path, re_path
from recipes.views import IngredientViewSet, RecipeViewSet, TagViewSet
from rest_framework.routers import DefaultRouter
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

# from django.urls import include, path
# from rest_framework.routers import DefaultRouter

# from api.views import UserViewSet
# from .views import IngredientViewSet, RecipeViewSet, TagViewSet

# router = DefaultRouter()
# router.register('users', UserViewSet, basename='user')
# router.register('recipes', RecipeViewSet, basename='recipes')
# router.register('tags', TagViewSet, basename='tags')
# router.register('ingredients', IngredientViewSet, basename='ingredients')

# urlpatterns = [
#     path('', include(router.urls)),
#     path('auth/', include('djoser.urls.authtoken')),
# ]

