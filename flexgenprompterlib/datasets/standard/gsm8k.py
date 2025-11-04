from flexgenprompterlib.interfaces.idataset import IDataset
from datasets import load_dataset

class GSM8KDataset(IDataset):
    def __init__(self, dataset_name=None):
        self.data = []
        self.load()
    
    def load(self):
        data = self._load_dataset("gsm8k", "main")["test"]
        for d in data:
            content = d["question"].strip()
            label = d["answer"].split("#### ")[-1]
            self.data.append({"content": content, "label": label})