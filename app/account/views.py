"""
Views for the account APIs.
"""

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes
)

from rest_framework import (
    viewsets,
    mixins,
    status,
)

from django_filters.rest_framework import DjangoFilterBackend


from utils.MultipleFieldLookupMixin import MultipleFieldLookupMixin

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from django.contrib.auth.decorators import login_required

from core.models import (
    Account,
    Feed,
    Friend,
    FriendRequest
)

from account import serializers


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'friend_requests',
                OpenApiTypes.STR,
                description='Comma separated list ofIDs to filter'
            ),
            OpenApiParameter(
                'friends',
                description='Comma separated list of IDs to filter.'
            )
        ]
    )
)
class AccountViewSet(viewsets.ModelViewSet):
    """View for managing account APIs."""

    serializer_class = serializers.AccountDetailSerializer
    queryset = Account.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']

    def _params_to_ints(self, qs):
        """Convert a list of strings to integers."""
        return [int(str_id) for str_id in qs.split(',')]

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.AccountSerializer
        elif self.action == 'upload_image':
            return serializers.AccountImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new account."""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to account."""
        account = self.get_object()
        serializer = self.get_serializer_class()(account, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.INT, enum=[0, 1],
                description='Filter by currently logged in user.',
            )
        ]
    )
)
class BaseAccountAttrViewSet(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Base viewset for account attributes"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class FriendViewSet(BaseAccountAttrViewSet):
    """Manage friends on account."""

    serializer_class = serializers.FriendSerializer
    queryset = Friend.objects.all()
