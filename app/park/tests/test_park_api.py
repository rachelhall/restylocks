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


def image_upload_url(park_id):
    """Create and return an image upload URL."""
    return reverse('park:park-upload-image', args=[park_id])


def create_park(user, **params):
    """Create and return a park."""
    defaults = {
        'name': 'Roller Skate Park',
        'street_number': 123,
        'street_name': 'Pershing',
        'street_suffix': 'W',
        'city': 'San Diego',
        'state': 'California',
        'postal_code': 92104,
        'country': 'United States',
        'description': 'Super fun skatepark',
    }
    defaults.update(params)

    park = Park.objects.create(user=user, **defaults)
    return park

    class ImageUploadTests(TestCase):
        """Tests for the image upload API."""

        def setUp(self):
            self.client = APIClient()
            self.user = get_user_model().objects.create_user(
                'user@example.com',
                'password1234'
            )
            self.client.force_authenticate(self.user)
            self.park = create_park(user=self.user)

        def tearDown(self):
            self.park.image.delete()

        def test_upload_image(self):
            """Test uploading an image to a recipe."""
            url = image_upload_url(self.park.id)
            with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
                img = Image.new(RGB, (10, 10))
                img.save(image_file, format='JPEG')
                image_file.seek(0)
                payload = {'image': image_file}
                res = self.client.post(url, payload, format='multipart')

            self.recipe.refresh_from_db()
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertIn('image', res.data)
            self.assertTrue(os.path.exists(self.park.image.path))

        def test_upload_image_bad_request(self):
            """Test uploading invalid image."""
            url = image_upload_url(self.park.id)
            payload = {'image': 'notanimage'}
            res = self.client.post(url, payload, format='multipart')
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
