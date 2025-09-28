from .base_dataset import BaseDataset

class GSM8KDataset(BaseDataset):
    def __init__(self):
        data = self._load_dataset("gsm8k", "main")["test"]
        self.data = []
        for d in data:
            content = d["question"].strip()
            label = d["answer"].split("#### ")[-1]
            self.data.append({"content": content, "label": label})