from .gsm8k_dataset import GSM8KDataset
from .csqa_dataset import CSQADataset
from .ecommerce_cls_dataset import EcommerceClassificationDataset

class DatasetBuilder:
    def __init__(self, dataset_name=None):
        self.dataset_name = dataset_name
        self.dataset_factory = {
            "gsm8k": GSM8KDataset,
            "csqa": CSQADataset,
            "ecommerce_classification": EcommerceClassificationDataset
        }

    def build(self):
        if self.dataset_name:
            dataset = self.dataset_factory.get(self.dataset_name)
            return dataset().data if dataset else None
        
        return None