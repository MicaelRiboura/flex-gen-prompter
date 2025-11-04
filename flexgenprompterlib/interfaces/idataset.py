import abc
from typing import List
from pydantic import BaseModel

class DatasetInfo(BaseModel):
    content: str
    label: str

class IDataset(abc.ABC):
    @abc.abstractmethod
    def load(self) -> List[DatasetInfo]:
        pass