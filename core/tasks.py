import time
from celery import shared_task

@shared_task(bind=True)
def long_running_task(self):
    # Simulação de uma tarefa longa
    total_steps = 300
    for i in range(total_steps):
        time.sleep(0.5) # Simula 1 segundo de trabalho
        # Você pode atualizar o estado da tarefa para fornecer feedback de progresso
        # current=i, total=total_steps, status='Processando...'
        current_step = i + 1
        print(f"Progresso: {current_step}/{total_steps}")
        self.update_state(state='PROGRESS',
                          meta={'current': current_step, 'total': total_steps})

    print("Processamento concluído!")
    return "Relatório gerado com sucesso!"
