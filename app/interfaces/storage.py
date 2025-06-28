from abc import ABC, abstractmethod

class Storage(ABC):
    
    @abstractmethod
    def save(self, filename: str, file: bytes) -> None:
        pass
    
    @abstractmethod
    def get(self, filename: str) -> None:
        pass