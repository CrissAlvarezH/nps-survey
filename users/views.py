# Rest framework
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
# Local
from .models import User
from .serializers import UserRetrieveSerializer, UserSerializer, UserSignUpSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserRetrieveSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        permissions = []

        if self.action in ['list', 'retrieve']:
            permissions = [IsAuthenticated]
        elif self.action in ['signup']:
            permissions = [AllowAny]

        return [p() for p in permissions]

    @action(detail=False, methods=['POST'])
    def signup(self, request, *args, **kwargs):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        user_json = UserSerializer(user).data
        return Response(user_json, status=status.HTTP_201_CREATED)
