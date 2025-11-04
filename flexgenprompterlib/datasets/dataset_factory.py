from .standard.gsm8k import GSM8KDataset
from .standard.csqa import CSQADataset
from .standard.ecommerce_classification import EcommerceClassificationDataset
from typing import List
from pydantic import BaseModel

class CustomDatasetData(BaseModel):
    name: str
    class_ref: type

class DatasetFactory:
    def __init__(self, dataset_name=None, custom_datasets: List[CustomDatasetData] = []):
        self.dataset_name = dataset_name
        self.dataset_factory = {
            "gsm8k": GSM8KDataset,
            # "csqa": CSQADataset,
            "ecommerce_classification": EcommerceClassificationDataset,
        }
        self.load_custom_datasets(custom_datasets)
    
    def load_custom_datasets(self, custom_datasets: List[CustomDatasetData]):
        for dataset in custom_datasets:
            self.dataset_factory[dataset.get('name')] = dataset.get('class_ref')

    def build(self):
        if self.dataset_name:
            dataset = self.dataset_factory.get(self.dataset_name)
            return dataset(dataset_name=self.dataset_name).data if dataset else None
        
        return None