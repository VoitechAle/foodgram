from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.response import Response
from api.serializers import UserSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # или настройте права доступа

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
