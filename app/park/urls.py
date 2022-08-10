""" 
URL mappings for the park app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from park import views

router = DefaultRouter()
router.register('parks', views.ParkViewSet)

app_name = 'park'

urlpatterns = [
    path('', include(router.urls))
]
