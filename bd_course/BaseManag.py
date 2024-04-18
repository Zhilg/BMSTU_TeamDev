from abc import abstractmethod
class BaseUserManag():
    @abstractmethod
    def __init__(self):
        self.rep = None
        pass
    @abstractmethod
    def create(self, form):
        pass
    @abstractmethod
    def create_superuser(self, form):
        pass
    @abstractmethod 
    def update_user(self, form):
        pass
    @abstractmethod 
    def get(self, form):
        pass
    
    @abstractmethod 
    def register_repository(self, rep):
        self.rep = rep
        pass
    

class BaseManag():
    @abstractmethod
    def __init__(self):
        self.rep = None
        pass
    
    @abstractmethod
    def get(self, form):
        pass
    
    @abstractmethod
    def create(self, form):
        pass
    
    @abstractmethod
    def unpack_field_values(self, form):
        pass
    
    @abstractmethod
    def get_meta_fields(self):
        pass
    
    @abstractmethod 
    def register_repository(self, rep):
        self.rep = rep
        pass