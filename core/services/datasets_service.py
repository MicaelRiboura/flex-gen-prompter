from flexgenprompterlib.datasets.dataset_factory import DatasetFactory

class DatasetsService:
    def list_datasets(self):
         datasets = DatasetFactory().dataset_factory.keys()
         return list(datasets)
    
    def get_dataset(self, dataset_name):
        dataset = DatasetFactory(dataset_name).build()
        return dataset