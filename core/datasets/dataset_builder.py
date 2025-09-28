from .gsm8k_dataset import GSM8KDataset
from .csqa_dataset import CSQADataset

class DatasetBuilder:
    def __init__(self, dataset_name=None):
        self.dataset_name = dataset_name
        self.dataset_factory = {
            "gsm8k": GSM8KDataset,
            "csqa": CSQADataset
        }

    def build(self):
        if not self.dataset_name:
            dataset = self.dataset_factory.get(self.dataset_name)
            return dataset() if dataset else None
        
        return None