from django.contrib import admin
from django.urls import path

from core.views import home, datasets

urlpatterns = [
    path('', home, name='home'),
    path('datasets/', datasets, name='datasets'),
]