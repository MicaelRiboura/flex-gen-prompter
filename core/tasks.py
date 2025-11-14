import time
from celery import shared_task
from core.evaluators.accuracy_evaluator import AccuracyEvaluator
from core.services.benchmark_service import BenchmarkService
from core.services.datasets_service import DatasetsService



@shared_task(bind=True)
def evaluate_workflows(self, model, dataset_name, techniques, sample):
    # result = AccuracyEvaluator(dataset_name, model, techniques).evaluate(
    #     num_samples=int(sample),
    #     update_state=self.update_state
    # )
    dataset_service = DatasetsService()
    dataset_data = dataset_service.get_dataset(dataset_name)

    benchmark_service = BenchmarkService()
    result = benchmark_service.evaluate(
        model=model,
        dataset_name=dataset_name,
        dataset_data=dataset_data,
        techniques=techniques,
        num_samples=int(sample),
        update_state=self.update_state
    )

    print("Avaliação concluída!")
    return result
