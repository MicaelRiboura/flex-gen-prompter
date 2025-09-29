from django.contrib import admin
from django.urls import path

from core.views import home, datasets, get_dataset_details

urlpatterns = [
    path('', home, name='home'),
    path('datasets/', datasets, name='datasets'),
    path('datasets/<str:dataset_name>/', get_dataset_details, name='dataset_details'),
]