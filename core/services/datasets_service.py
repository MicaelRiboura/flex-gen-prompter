import pandas as pd
from flexgenprompterlib import DatasetFactory
from flexgenprompterlib.interfaces.idataset import IDataset
from core.models import Dataset

class CustomDataset(IDataset):
    @classmethod
    def register_dataset_name(cls, dataset_name: str):
        cls.dataset_name = dataset_name
    
    def load(self):
        dataset_file = Dataset.objects.filter(name=CustomDataset.dataset_name).first().filename
        df = pd.read_csv(f'media/uploads/{dataset_file}', index_col=0)
        self.data = [{"content": row[0], "label": row[1]} for _, row in df.iterrows()]

        return self.data

class DatasetsService:
    def _load_datasets(self):
        datasets = Dataset.objects.all()
        for dataset in datasets:
            CustomDataset.register_dataset_name(dataset.name)
            DatasetFactory.register(
                name=dataset.name,
                class_ref=CustomDataset
            )

    def list_datasets(self):
         self._load_datasets()
         datasets = DatasetFactory.dataset_factory.keys()
         return list(datasets)
    
    def get_dataset(self, dataset_name):
        dataset = DatasetFactory.get(dataset_name)
        return dataset