from teamdev.BaseRepFactory import BaseRepFactory
from lms.repositories.repositories import *

class PgRepFactory(BaseRepFactory):
    def __init__(self):
        pass
    
    def UserProfilesRep(self):
        return UserProfilesRepository()
    
    def TasksRep(self):
        return TasksRepository()
    
    def TaskPacksRep(self):
        return TaskPacksRepository()
    
    def SolutionsRep(self):
        return SolutionsRepository()