""" 
Serializers for account APIs.
"""

from rest_framework import serializers


from core.models import (
    Account,
    Feed,
    Friend,
    FriendRequest,
)


class FriendSerializer(serializers.ModelSerializer):
    """Serializer for adding and removing friends."""

    class Meta:
        model = Friend
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class FriendRequestSerializer(serializers.ModelSerializer):
    """Serializer for sending friend request."""

    class Meta:
        model = FriendRequest
        fields = ['to_user', 'from_user', 'created_at']


class AccountSerializer(serializers.ModelSerializer):
    """Serializer for account."""

    friends = FriendSerializer(many=True, required=False)

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

    def _get_or_create_friends(self, friends, account):
        """Handle getting or creating friends as needed."""
        auth_user = self.context['request'].user
        for friend in friends:
            friend_obj, created = Friend.objects.get_or_create(
                user=auth_user,
                **friend
            )
            account.friends.add(friend_obj)

    def create(self, validated_data):
        """Create an account."""
        friends = validated_data.pop('friends', [])
        account = Account.objects.create(**validated_data)
        self._get_or_create_friends(friends, account)

        return account

    def update(self, instance, validated_data):
        """Update acccount."""
        friends = validated_data.pop('friends', None)
        if friends is not None:
            instance.friends.clear()
            self._get_or_create_friends(friends, account)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class AccountDetailSerializer(AccountSerializer):
    """Serializer for account detail view."""

    class Meta(AccountSerializer.Meta):
        fields = AccountSerializer.Meta.fields + ['description', 'image']


class AccountImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading image to account."""

    class Meta:
        model = Account
        fields = ['id', 'avatar']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': True}}
