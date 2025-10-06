from .base_dataset import BaseDataset
import pandas as pd

class EcommerceClassificationDataset(BaseDataset):
    def __init__(self):
        data = pd.read_csv('core/datasets/ecommerceDataset.csv')
        self.data = []
        for i, row in data.iterrows():
            content = row[1]
            label = row[0]
            self.data.append({"content": content, "label": label})