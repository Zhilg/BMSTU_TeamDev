from abc import ABC, abstractmethod

class BaseRepFactory(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def UserProfilesRep(self):
        pass
    
    @abstractmethod
    def TasksRep(self):
        pass
    
    @abstractmethod
    def TaskPacksRep(self):
        pass
    
    @abstractmethod
    def SolutionsRep(self):
        pass