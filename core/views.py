from django.shortcuts import render
from .services.datasets_service import DatasetsService
from django.core.paginator import Paginator
from core.prompting_techniques.workflow_factory import WorflowFactory
from django.http import JsonResponse
from .tasks import long_running_task
from celery.result import AsyncResult

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


def start_evaluation(request):

    task = long_running_task.delay()

    return JsonResponse({
        'message': 'Seu processamento foi iniciado! Você será notificado quando terminar.',
        'task_id': task.id
    }, status=202) # Sta


def check_evaluation_status(request, task_id):
    task_result = AsyncResult(task_id)

    response_data = {
        'task_id': task_id,
        'status': task_result.status,
        'result': None,
        'error': None,
        'progress': {'current': 0, 'total': 100, 'percent': 0}
    }

    if task_result.status == 'SUCCESS':
        response_data['result'] = task_result.result
        response_data['progress']['current'] = 100
        response_data['progress']['percent'] = 100

    elif task_result.status == 'FAILURE':
        response_data['error'] = str(task_result.info) # Erros ficam em .info quando há falha
        response_data['progress']['percent'] = 0

    elif task_result.status == 'PROGRESS':
        # Aqui está a mágica: lemos os metadados de .info
        progress_info = task_result.info
        current = progress_info.get('current', 0)
        total = progress_info.get('total', 1) # Evitar divisão por zero

        response_data['progress']['current'] = current
        response_data['progress']['total'] = total
        response_data['progress']['percent'] = (current / total) * 100

    # Para outros estados como PENDING, a resposta padrão já serve.

    return JsonResponse(response_data)