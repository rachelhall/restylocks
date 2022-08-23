""" 
Tests for account APIs.
"""


# from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from utils.create_test_user import create_user

from core.models import (
    User,
    Account
)

from account.serializers import (
    AccountSerializer
)

ACCOUNTS_URL = reverse('account:account-list')


def image_upload_url(account_id):
    """Create and return an image upload URL."""
    return reverse('account:account-upload-image', args=[account_id])


def create_account(user, **params):
    """Create and return a sample account."""
    defaults = {
        'name': "Test name",
        'pronouns': 'she/her',
        'bio': 'Test account bio'
    }
    defaults.update(params)

    account = Account.objects.create(user=user, **defaults)
    return account


class PublicAccountAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(ACCOUNTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAccountAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)

    def test_retrieve_account(self):
        create_account(user=self.user)

        res = self.client.get(ACCOUNTS_URL)

        accounts = Account.objects.all().order_by('-id')
        serializer = AccountSerializer(accounts, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
