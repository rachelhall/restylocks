""" 
Tests for park API
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


PARKS_URL = reverse('park:park-list')


def detail_url(park_id):
    """Create and return a park detail URL."""
    return reverse('park:park-detail', args=[park_id])


def create_park(user, **params):
    """Create and return a park."""
    defaults = {
        'name': 'Roller Skate Park',
        'city': 'San Diego',
        'state': 'California',
        'description': 'Super fun skatepark',
    }
    defaults.update(params)

    park = Park.objects.create(user=user, **defaults)
    return park
