
from teamdev.PgRepFactory import PgRepFactory
from lms.managers.managers import *

factory = PgRepFactory()

UPR = factory.UserProfilesRep()
TR = factory.TasksRep()
TPR = factory.TaskPacksRep()
SR = factory.SolutionsRep()

UPM = UserProfilesManager()
UPM.register_repository(UPR)

TM = TasksManager()
TM.register_repository(TR)

TPM = TaskPacksManager()
TPM.register_repository(TPR)

SM = SolutionsManager()
SM.register_repository(SR)