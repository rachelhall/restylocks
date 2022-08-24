""" 
Serializers for account APIs.
"""

from rest_framework import serializers


from core.models import (
    Account,
    FriendRequest,
    Feed
)


class AccountSerializer(serializers.ModelSerializer):
    """Serializer for account."""

    class Meta:
        model = Account
        fields = [
            'id',
            'user',
            'name',
            'pronouns',
            'avatar',
            'bio',
            'friends',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create an account."""
        friends = validated_data.pop('friends', [])
        account = Account.objects.create(**validated_data)

        return account

    def update(self, instance, validated_data):
        """Update acccount."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class AccountDetailSerializer(AccountSerializer):
    """Serializer for account detail view."""

    class Meta(AccountSerializer.Meta):
        fields = AccountSerializer.Meta.fields


class AccountImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading image to account."""

    class Meta:
        model = Account
        fields = ['id', 'avatar']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': True}}


class FriendSerializer(serializers.ModelSerializer):
    """Serializer for adding and removing friends."""

    class Meta:
        model = Account
        fields = ['friends']


class FriendRequestSerializer(serializers.ModelSerializer):
    """Serializer for sending friend request."""

    class Meta:
        model = FriendRequest
        fields = ['to_user', 'from_user', 'created_at']
