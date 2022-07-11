"""
URL mappings for the userAPI
"""
from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create')
]
