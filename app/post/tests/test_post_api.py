""" 
Test for post API.
"""

from decimal import Decimal
import tempfile
import os

from PIL import Image

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Post,
    Park,
)

from post.serializers import PostSerializer

POSTS_URL = reverse('post:post-list')


def image_upload_url(post_id):
    """Create and return an image upload URL."""
    return reverse('post:post-upload-image', args=[post_id])


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


def create_post(user, **params):
    """Create and return a sample post"""

    park = Park.objects.create(
        user=user,
        name='Sample park',
        street_number=124,
        street_name='Covington',
        city='San Diego',
        state='California',
        country='United States',
        description='Really cool park'
    )

    defaults = {
        'title': 'Sample post title',
        'park': park,
        'description': 'A very nice post',
    }
    defaults.update(params)

    post = Post.objects.create(user=user, **defaults)
    return post


class PublicPostAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(POSTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePostAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com',
            password='testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_posts(self):
        """Test retreiving a list of posts"""
        create_post(user=self.user)
        create_post(user=self.user)

        res = self.client.get(POSTS_URL)

        all_posts = Post.objects.all().order_by('-id')
        serializer = PostSerializer(all_posts, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_post_list_limited_to_user(self):
        """Test list of posts is limited to authenticated user."""
        other_user = create_user(
            email='other@example.com',
            password='password123',
        )
        create_post(user=other_user)
        create_post(user=self.user)

        res = self.client.get(POSTS_URL)

        all_posts = Post.objects.filter(user=self.user)
        serializer = PostSerializer(all_posts, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class ImageUploadTests(TestCase):
    """Tests for the image upload API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)
        self.post = create_post(user=self.user)

    def tearDown(self):
        self.post.image.delete()

    def test_upload_image(self):
        """Test uploading an image to a post."""
        url = image_upload_url(self.post.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file}
            res = self.client.post(url, payload, format='multipart')

        self.post.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.post.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading invalid image."""
        url = image_upload_url(self.post.id)
        payload = {'image': 'notanimage'}
        res = self.client.post(url, payload, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
