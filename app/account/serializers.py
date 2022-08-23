""" 
Serializers for account APIs.
"""

from rest_framework import serializers


from core.models import (
    Account
)


class AccountSerializer(serializers.ModelSerializer):
    """Serializer for account."""

    class Meta:
        model = Account
        fields = [
            'user',
            'name',
            'pronouns',
            'avatar',
            'bio'
        ]

    def create(self, validated_data):
        """Create an account."""
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
