"""
Serializers for post APIs
"""

from rest_framework import serializers

from core.models import Post


class PostSerializer(serializers.ModelSerializer):
    """Serializer for posts."""

    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'title',
            'description',
            'park',
            'image',
        ]
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        """Create a post."""
        post = Post.objects.create(**validated_data)

        return post

    def update(self, instance, validated_data):
        """Update post"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class PostDetailSerializer(PostSerializer):
    """Serializer for post detail view."""

    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ['description', 'image']


class PostImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading image to posts."""

    class Meta:
        model = Post
        fields = ['id', 'image']
        read_only_fields = ['id']
