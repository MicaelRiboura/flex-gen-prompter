from flexgenprompterlib.interfaces.idataset import IDataset
import pandas as pd

class EcommerceClassificationDataset(IDataset):
    def __init__(self):
        self.data = [] 
        self.load()
    
    def load(self):
        df = pd.read_csv('flexgenprompterlib/datasets/data/ecommerceDataset.csv')
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        for i, row in df.iterrows():
            content = row[1]
            label = row[0]
            self.data.append({"content": content, "label": label})