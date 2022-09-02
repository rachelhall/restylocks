"""
URL mappings for the account app.
"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from account import views

router = DefaultRouter()
router.register('accounts', views.AccountViewSet)
router.register('friends', views.FriendViewSet)

app_name = 'account'

urlpatterns = [
    path('', include(router.urls))
]
