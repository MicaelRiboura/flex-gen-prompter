from dotenv import load_dotenv
load_dotenv()
from flexgenprompterlib.techniques import WorkflowFactory
from flexgenprompterlib import DatasetFactory
from flexgenprompterlib.interfaces.idataset import IDataset

# class DatasetCustom(IDataset):
#     def __init__(self):
#         self.data = []
    
#     def load(self):
#         self.data = [
#             {"content": "This is a custom dataset example.", "label": "example"}
#         ]

#         return self.data

# dataset_class: IDataset = DatasetCustom

# DatasetFactory.register(
#     name='custom_ecommerce',
#     class_ref=dataset_class
# )

# response = DatasetFactory.get('custom_ecommerce')
# print(response)

workflow = WorkflowFactory(
    model='gpt-4.1',
    dataset_name='gsm8k'
).create_workflow('zero_shot')

response = workflow.run(prompt="What is 1234 multiplied by 5678?")

print('response: ', response)