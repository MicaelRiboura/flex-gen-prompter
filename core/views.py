from django.shortcuts import render
from .services.datasets_service import DatasetsService
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    service = DatasetsService()
    datasets = service.list_datasets()
    return render(request, 'home.html', {'datasets': datasets})


def datasets(request):
    service = DatasetsService()
    datasets = service.list_datasets()
    return render(request, 'datasets.html', {'datasets': datasets})

def get_dataset_details(request, dataset_name):
    service = DatasetsService()
    dataset = service.get_dataset(dataset_name)

    page_number = request.GET.get('page', 1)
    paginator = Paginator(dataset, 10)  # Show 10 records per page
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'dataset_details.html', {
        'dataset': dataset_name,
        'page_obj': page_obj
    })