from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password)


class AccountModelTests(TestCase):
    """Test account Model"""

    def test_create_account(self):
        """Test creating a account."""

        user = create_user()
        account = models.Account.objects.create(
            user=user,
            name='First Last',
            pronouns='She/her',
            bio="Sample bio",
        )

    @patch('core.models.uuid.uuid4')
    def test_account_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.account_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/account/{uuid}.jpg')
