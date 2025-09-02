# api/serializers.py
from recipes.models import Ingredient, Recipe, ShoppingCart, Tag
from rest_framework import serializers
from users.models import Favorite, Follow, User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient', queryset=Ingredient.objects.all()
    )
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True)

    class Meta:
        model = Recipe.recipe_ingredients.rel.related_model
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeCRUDSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    ingredients = RecipeIngredientSerializer(
        source='recipe_ingredients', many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)
    cooking_time = serializers.IntegerField(min_value=1)

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'title', 'image', 'description',
                  'ingredients', 'tags', 'cooking_time')

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError("Нужно указать ингредиенты")
        ingredients_ids = [item['ingredient'].id for item in value]
        if len(set(ingredients_ids)) != len(ingredients_ids):
            raise serializers.ValidationError(
                "Ингредиенты должны быть уникальными")
        for item in value:
            if item.get('amount', 0) <= 0:
                raise serializers.ValidationError(
                    "Количество ингредиента должно быть положительным")
        return value

    def create(self, validated_data):
        # ingredients_data = validated_data.pop('recipe_ingredients', [])
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags_data)
        for ingredient_data in ingredients:
            ingredient = ingredient_data['ingredient']
            amount = ingredient_data['amount']
            recipe.recipe_ingredients.create(
                ingredient=ingredient, amount=amount)
        return recipe

    def update(self, instance, validated_data):
        # ingredients_data = validated_data.pop('recipe_ingredients')
        tags_data = validated_data.pop('tags')
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.save()
        instance.tags.set(tags_data)
        instance.recipe_ingredients.all().delete()
        for ingredient_data in ingredients:
            ingredient = ingredient_data['ingredient']
            amount = ingredient_data['amount']
            instance.recipe_ingredients.create(
                ingredient=ingredient, amount=amount)
        return instance


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    recipe = serializers.StringRelatedField(read_only=True)
    recipe_id = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(), write_only=True)

    class Meta:
        model = Favorite
        fields = ('user', 'recipe', 'recipe_id')

    def create(self, validated_data):
        user = self.context['request'].user
        recipe = validated_data['recipe_id']
        return Favorite.objects.create(user=user, recipe=recipe)


class ShoppingCartSerializer(serializers.ModelSerializer):
    cart_owner = serializers.StringRelatedField(read_only=True)
    recipe = serializers.StringRelatedField(read_only=True)
    recipe_id = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(), write_only=True)

    class Meta:
        model = ShoppingCart
        fields = ('cart_owner', 'recipe', 'recipe_id')

    def create(self, validated_data):
        user = self.context['request'].user
        recipe = validated_data['recipe_id']
        return ShoppingCart.objects.create(cart_owner=user, recipe=recipe)


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class SubscribeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    author = UserShortSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ('user', 'author')

    def validate(self, data):
        user = self.context['request'].user
        author = self.instance.author if self.instance else None
        if author is None and 'author' in self.initial:
            author_id = self.initial_data.get('author')
            author = User.objects.filter(pk=author_id).first()
        if user == author:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя")
        if Follow.objects.filter(user=user,
                                 author=author).exists():
            raise serializers.ValidationError(
                "Вы уже подписаны на этого пользователя")
        return data


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    avatar = serializers.ImageField(read_only=True)  # Если есть поле avatar

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name',
            'last_name', 'email', 'is_subscribed', 'avatar')

    def get_is_subscribed(self, obj):
        request = self.context.get('request', None)
        user = request.user if request else None
        if user and user.is_authenticated:
            return Follow.objects.filter(
                user=user, author=obj).exists()
        return False
