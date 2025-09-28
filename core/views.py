from django.shortcuts import render
from .services.datasets_service import DatasetsService

# Create your views here.
def home(request):
    service = DatasetsService()
    datasets = service.list_datasets()
    return render(request, 'home.html', {'datasets': datasets})


def datasets(request):
    service = DatasetsService()
    datasets = service.list_datasets()
    return render(request, 'datasets.html', {'datasets': datasets})