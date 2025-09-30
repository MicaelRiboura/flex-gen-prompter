import time
from celery import shared_task
from core.evaluators.accuracy_evaluator import AccuracyEvaluator



@shared_task(bind=True)
def evaluate_workflows(self, model, dataset, techniques, sample):
    result = AccuracyEvaluator(dataset, model, techniques).evaluate(
        num_samples=int(sample),
        update_state=self.update_state
    )

    print("Avaliação concluída!")
    return result
