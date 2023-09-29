from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as f
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import User
from .permissions import NotAuthenticatedOrAdmin, IsOwnerAdminOrReadOnly
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.filter(is_active=True)

    permission_classes = (IsAuthenticated, IsOwnerAdminOrReadOnly)

    serializer_class = UserSerializer

    http_method_names = ('get', 'post', 'patch', 'head', 'options', 'delete')

    filter_backends = (f.OrderingFilter, DjangoFilterBackend)

    ordering_fields = ('username', 'email', 'date_joined')

    filterset_fields = ('is_staff',)

    def get_permissions(self):
        if self.action == 'create':
            return [NotAuthenticatedOrAdmin()]
        return super().get_permissions()
