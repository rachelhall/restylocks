"""
Serializers for post APIs
"""

from rest_framework import serializers

from core.models import (
    Post,
    Tag,
)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class PostSerializer(serializers.ModelSerializer):
    """Serializer for posts."""

    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'account',
            'title',
            'description',
            'park',
            'image',
            'tags'
        ]
        read_only_fields = ['id', 'user', 'account']

    def _get_or_create_tags(self, tags, post):
        """Handle getting or creating tags as needed."""
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            post.tags.add(tag_obj)

    def create(self, validated_data):
        """Create a post."""
        tags = validated_data.pop('tags', [])
        post = Post.objects.create(**validated_data)
        account = self.account.id
        self._get_or_create_tags(tags, post)

        return post

    def update(self, instance, validated_data):
        """Update post"""
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class PostDetailSerializer(PostSerializer):
    """Serializer for post detail view."""

    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + \
            ['account', 'description', 'image']


class PostImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading image to posts."""

    class Meta:
        model = Post
        fields = ['id', 'image']
        read_only_fields = ['id']
