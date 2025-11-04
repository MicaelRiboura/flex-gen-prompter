from dotenv import load_dotenv
load_dotenv()
from flexgenprompterlib.techniques import WorkflowFactory

workflow = WorkflowFactory(
    model='gpt-4.1',
    dataset_name='gsm8k'
).create_workflow('zero_shot')

response = workflow.run(prompt="What is 1234 multiplied by 5678?")

print('response: ', response)