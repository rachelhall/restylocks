""" 
Serializers for park APIs
"""

from rest_framework import serializers

from core.models import (
    Park,
)


class ParkSerializer(serializers.ModelSerializer):
    """Serializer for parks."""

    class Meta:
        model = Park
        fields = [
            'id',
            'name',
            'street_number',
            'street_name',
            'city',
            'state',
            'postal_code',
            'country',
            'description',
            'image'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a park."""
        park = Park.objects.create(**validated_data)

        return park

    def update(self, instance, validated_data):
        """Update park."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class ParkDetailSerializer(ParkSerializer):
    """Serializer for park detail view."""

    class Meta(ParkSerializer.Meta):
        fields = ParkSerializer.Meta.fields + ['description', 'image']


class ParkImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading image to parks."""

    class Meta:
        model = Park
        fields = ['id', 'image']
        read_only_fields = ['id']
