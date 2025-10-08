from django.contrib import admin
from django.urls import path

from core.views import home, datasets, get_dataset_details, start_evaluation, check_evaluation_status, upload_dataset_csv

urlpatterns = [
    path('', home, name='home'),
    path('datasets/', datasets, name='datasets'),
    path('datasets/<str:dataset_name>/', get_dataset_details, name='dataset_details'),
    path('evaluation/', start_evaluation, name='start_evaluation'),
    path('evaluation/check/<str:task_id>/', check_evaluation_status, name='check_evaluation_status'),
    path('upload/', upload_dataset_csv),
]