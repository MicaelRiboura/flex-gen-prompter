from django.shortcuts import render
from .services.datasets_service import DatasetsService
from django.core.paginator import Paginator
from django.http import JsonResponse
from .tasks import evaluate_workflows
from celery.result import AsyncResult
from django.views.decorators.http import require_POST
from core.prompting_techniques.workflow_factory import WorkflowFactory
import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from core.models import Dataset
import pandas as pd

# Create your views here.
def home(request):
    service = DatasetsService()
    datasets = service.list_datasets()
    custom_datasets = list(Dataset.objects.values_list('name', flat=True))
    datasets.extend(custom_datasets)
    techniques = WorkflowFactory(model=None).workflow_factory.keys()
    return render(request, 'home.html', {'datasets': datasets, 'techniques': techniques })


def datasets(request):
    service = DatasetsService()
    datasets = service.list_datasets()
    custom_datasets = list(Dataset.objects.values_list('name', flat=True))
    datasets.extend(custom_datasets)
    return render(request, 'datasets.html', {'datasets': datasets})

def get_dataset_details(request, dataset_name):
    service = DatasetsService()
    if dataset_name in service.list_datasets():
        dataset = service.get_dataset(dataset_name)
    else:
        dataset = []
        dataset_object = Dataset.objects.filter(name=dataset_name).first()
        if dataset_object:
            df = pd.read_csv(f'media/uploads/{dataset_object.filename}')
            for i, row in df.iterrows():
                content = row['content']
                label = row['label']
                dataset.append({ 'content': content, 'label': label })
                

    page_number = request.GET.get('page', 1)
    paginator = Paginator(dataset, 10)  # Show 10 records per page
    page_obj = paginator.get_page(page_number)

    return render(request, 'dataset_details.html', {
        'dataset': dataset_name,
        'page_obj': page_obj
    })

@require_POST
def start_evaluation(request):
    dataset_name = request.POST.get('dataset')
    model = request.POST.get('model')
    techniques = request.POST.getlist('techniques')
    sample = request.POST.get('sample')
    print('request.POST.dataset_name: ', dataset_name)
    print('request.POST.model: ', model)
    print('request.POST.techniques: ', techniques)
    print('request.POST.sample: ', sample)

    task = evaluate_workflows.delay(model, dataset_name, techniques, sample)

    return JsonResponse({
        'message': 'Seu processamento foi iniciado! Você será notificado quando terminar.',
        'task_id': task.id
    }, status=202)


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


@csrf_exempt  # For simplicity, better use proper CSRF in production
def upload_dataset_csv(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']

        # Create folder if not exists
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)

        # Save file
        file_path = os.path.join(upload_dir, file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
                
        dataset_name = file.name.replace('.csv', '')
        if Dataset.objects.filter(name=dataset_name).count() > 0:
            return JsonResponse({'message': 'Dataset editado com sucesso!', 'filename': file.name})
        
        Dataset.objects.create(
            name=dataset_name, 
            filename=file.name
        )

        return JsonResponse({'message': 'Dataset carregado com sucesso!', 'filename': file.name})

    return JsonResponse({'error': 'Invalid request'}, status=400)