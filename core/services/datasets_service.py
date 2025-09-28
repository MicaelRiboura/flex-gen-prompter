from core.datasets.dataset_builder import DatasetBuilder

class DatasetsService:
    def list_datasets(self):
         datasets = DatasetBuilder().dataset_factory.keys()
         return list(datasets)
    
    def get_dataset(self, dataset_name):
        dataset = DatasetBuilder(dataset_name).build()
        return dataset