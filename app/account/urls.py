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
router.register('account', views.AccountViewSet)

app_name = 'account'

urlpatterns = [
    path('', include(router.urls))
]
