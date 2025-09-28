from datasets import load_dataset

class BaseDataset:
    def __init__(self):
        self.data = []
    
    def _load_dataset(self, path, name):
        dataset = load_dataset(path, name)
        return  dataset