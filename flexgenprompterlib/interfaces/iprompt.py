from abc import ABC, abstractmethod

class IPrompt(ABC):
    @abstractmethod
    def get(self, node: str, dataset: str) -> str:
        pass

    @abstractmethod
    def register(self, node: str, dataset: str, content: str):
        pass