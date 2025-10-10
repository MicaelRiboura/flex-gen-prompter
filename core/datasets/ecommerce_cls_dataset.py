from .base_dataset import BaseDataset
import pandas as pd

class EcommerceClassificationDataset(BaseDataset):
    def __init__(self):
        df = pd.read_csv('core/datasets/ecommerceDataset.csv')
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        self.data = []
        for i, row in df.iterrows():
            content = row[1]
            label = row[0]
            self.data.append({"content": content, "label": label})