"""
Database models.
"""
import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone

from autoslug import AutoSlugField


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'recipe', filename)


def park_image_file_path(instance, filename):
    """Generate file path for new park image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'park', filename)


def post_image_file_path(instance, filename):
    """Generate file path for new park image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'post', filename)


def account_image_file_path(instance, filename):
    """Generate file path for new account image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'account', filename)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class FriendRequest(models.Model):
    """Information about an accounts friend requests"""
    to_user = models.ForeignKey(
        User, related_name='to_user', on_delete=models.CASCADE
    )
    from_user = models.ForeignKey(
        User, related_name='from_user', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "From {}, to {}".format((self.from_user.username, self.to_user.username))


class Account(models.Model):
    """Profile information for user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    pronouns = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(
        null=True,
        upload_to=account_image_file_path
    )
    bio = models.TextField(max_length=255)
    friends = models.ManyToManyField('Friend')

    def __string__(self):
        return f'{self.user.name} Account'


class Friend(models.Model):
    """Friend class"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name


class Feed(models.Model):
    """Account feed."""

    def __string__(self):
        return 'Feed'


class Park(models.Model):
    """Skate park object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    street_number = models.IntegerField(null=True)
    street_name = models.CharField(blank=True, max_length=255)
    street_suffix = models.CharField(blank=True, max_length=255)
    city = models.CharField(blank=True, max_length=255)
    state = models.CharField(blank=True, max_length=255)
    postal_code = models.IntegerField(null=True)
    country = models.CharField(max_length=255, default='United States')
    description = models.TextField(blank=True)
    image = models.ImageField(
        null=True, upload_to=park_image_file_path)

    def __str__(self):
        return self.name


class Post(models.Model):
    """Post object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    account = models.ForeignKey(
        Account, on_delete=models.DO_NOTHING, null=True)
    title = models.CharField(max_length=255)
    park = models.ForeignKey(Park, on_delete=models.CASCADE, null=True)
    description = models.TextField(blank=True)
    image = models.ImageField(
        null=True, upload_to=post_image_file_path)
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title


class Comments(models.Model):
    """Comment object."""
    post = models.ForeignKey(
        Post, related_name='details', on_delete=models.CASCADE, null=True)
    park = models.ForeignKey(Park, related_name='details',
                             on_delete=models.CASCADE, null=True)
    username = models.ForeignKey(
        User, related_name='details', on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    comment_date = models.DateTimeField(default=timezone.now)

    def __str___(self):
        return self.comment


class Recipe(models.Model):
    """Recipe object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient')
    image = models.ImageField(
        null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title


class Tag(models.Model):
    """Tag for filter skate parks"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient for recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
