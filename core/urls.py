from django.contrib import admin
from django.urls import path

from core.views import (
    home, 
    datasets, 
    datasets_json, 
    get_dataset_details, 
    start_evaluation, 
    check_evaluation_status, 
    upload_dataset_csv, 
    get_prompts, 
    get_nodes_framework, 
    update_prompt
)

urlpatterns = [
    path('', home, name='home'),
    path('datasets/', datasets, name='datasets'),
    path('datasets-data/', datasets_json, name='datasets_json'),
    path('datasets/<str:dataset_name>/', get_dataset_details, name='dataset_details'),
    path('evaluation/', start_evaluation, name='start_evaluation'),
    path('evaluation/check/<str:task_id>/', check_evaluation_status, name='check_evaluation_status'),
    path('upload/', upload_dataset_csv),
    path('prompts/', get_prompts, name='get_prompts'),
    path('prompts-data/', get_nodes_framework, name='get_nodes_framework'),
    path('update_prompt/', update_prompt, name='update_prompt'),
]