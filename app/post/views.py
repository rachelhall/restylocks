"""
Views for the post APIs.
"""
from rest_framework import (
    viewsets,
    status,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action


from core.models import Post
from post import serializers


class PostViewSet(viewsets.ModelViewSet):
    """View for managing post APIs."""
    serializer_class = serializers.PostDetailSerializer
    queryset = Post.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve posts for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer for the request."""
        if self.action == 'list':
            return serializers.PostSerializer
        elif self.action == 'upload_image':
            return serializers.PostImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create new post."""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload image to post"""
        post = self.get_object()
        serializer = self.get_serializer_class()(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
