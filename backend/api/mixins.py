from rest_framework import mixins, status
from rest_framework.response import Response


class CustomListRecipeDeleteMixin(mixins.ListModelMixin,
                                  mixins.DestroyModelMixin):

    def destroy(self, request, *args, **kwargs):
        model = kwargs.get('model')
        fkey = kwargs.get('fkey')
        recipe_id = self.kwargs.get('recipe_id')
        user = request.user
        instance = (model.objects.filter(**{fkey: user},
                    recipe__id=recipe_id).first())
        if instance is None:
            return Response(
                {'detail': 'Объект не найден'},
                status=status.HTTP_404_NOT_FOUND)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
