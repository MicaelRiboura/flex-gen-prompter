from flexgenprompterlib import DatasetFactory

class DatasetsService:
    def list_datasets(self):
         datasets = DatasetFactory.dataset_factory.keys()
         return list(datasets)
    
    def get_dataset(self, dataset_name):
        dataset = DatasetFactory.get(dataset_name)
        return dataset