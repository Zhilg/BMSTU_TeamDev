from abc import ABC, abstractmethod

class BaseRep(ABC):
    @abstractmethod 
    def insert(self, obj):
        pass
    
    @abstractmethod
    def update(self, obj):
        pass
    
    @abstractmethod
    def get(self, obj):
        pass