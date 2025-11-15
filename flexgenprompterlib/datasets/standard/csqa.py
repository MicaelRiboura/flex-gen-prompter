from flexgenprompterlib.interfaces.idataset import IDataset
from datasets import load_dataset

class CSQADataset(IDataset):
    def __init__(self):
        self.data = []

    def load(self):
        data = load_dataset("commonsense_qa", "default")["validation"]
        choice_index = ['A','B','C','D','E']
        for d in data:
            raw_q = d["question"].strip()
            choice = "\nAnswer Choices:"
            choice_list = d["choices"]["text"]
            for i, c in enumerate(choice_list):
                choice += " ("
                choice += choice_index[i]
                choice += ") "
                choice += c
            q = raw_q + " " + choice
            a = d["answerKey"]
            self.data.append({"content": q, "label": a})

        return self.data