from .standard.gsm8k import GSM8KDataset
from .standard.csqa import CSQADataset
from .standard.ecommerce_classification import EcommerceClassificationDataset
from flexgenprompterlib.interfaces.idataset import IDataset

class DatasetFactory:
    dataset_factory = {
        "gsm8k": GSM8KDataset,
        # "csqa": CSQADataset,
        "ecommerce_classification": EcommerceClassificationDataset,
    }
    
    @classmethod
    def register(cls, name: str, class_ref: IDataset):
        cls.dataset_factory[name] = class_ref

    @classmethod
    def clear(cls):
        cls.dataset_factory = {
            "gsm8k": GSM8KDataset,
            # "csqa": CSQADataset,
            "ecommerce_classification": EcommerceClassificationDataset,
        }

    @classmethod
    def get(cls, dataset_name: str):
        dataset_class = cls.dataset_factory.get(dataset_name)
        return dataset_class().load() if dataset_class else None