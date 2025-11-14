from flexgenprompterlib.interfaces.idataset import IDataset
from datasets import load_dataset

class GSM8KDataset(IDataset):
    def __init__(self):
        self.data = []
    
    def load(self):
        data = load_dataset("gsm8k", "main")["test"]
        for d in data:
            content = d["question"].strip()
            label = d["answer"].split("#### ")[-1]
            self.data.append({"content": content, "label": label})
        
        return self.data