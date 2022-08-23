"""
Views for the account APIs.
"""

from rest_framework import (
    viewsets,
    mixins,
    status,
)

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Account
)

from account import serializers


class AccountViewSet(viewsets.ModelViewSet):
    """View for managing account APIs."""
    serializer_class = serializers.AccountDetailSerializer
    queryset = Account.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, qs):
        """Convert a list of strings to integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retreive accounts."""
        queryset = self.queryset
        return queryset.filter(user=self.request.user).order_by('-id').distinct()

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
