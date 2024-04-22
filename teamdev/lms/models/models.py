from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.hashers import make_password, check_password

class Tasks(models.Model):
    filename = models.CharField(max_length=100, unique=True)
    theme = models.CharField(max_length=100)

class UserProfiles(AbstractBaseUser):
    '''
    Класс UserProfiles является моделью пользователя, представляющей пользовательский профиль в системе.
    Он наследует от AbstractBaseUser, что позволяет определить собственную модель пользователя.
    '''
    last_login = models.DateTimeField(auto_now=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    grup = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_authenticated = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff
    
class TaskPacks(models.Model):
    '''
    Класс TaskPacks является моделью комплекта задач, представляющей комплект задач в системе.
    Он наследует от AbstractBaseUser, что позволяет определить собственную модель комплекта задач.
    '''
    tasks = models.ManyToManyField(Tasks)
    student = models.ForeignKey(UserProfiles, on_delete=models.CASCADE, related_name='student_taskpacks')
    teacher = models.ForeignKey(UserProfiles, on_delete=models.CASCADE, related_name='teacher_taskpacks')
    maxgrade = models.IntegerField()
    mingrade = models.IntegerField()
    duetime = models.DateField()
    
class Solutions(models.Model):
    '''
    Класс Solutions является моделью решений, представляющей решение в системе.
    Он наследует от AbstractBaseUser, что позволяет определить собственную модель решений.
    '''
    student = models.ForeignKey(UserProfiles, on_delete=models.CASCADE, related_name='student_solutions')
    teacher = models.ForeignKey(UserProfiles, on_delete=models.CASCADE, related_name='teacher_solutions')
    taskpack = models.ForeignKey(TaskPacks, on_delete=models.CASCADE)
    grade = models.IntegerField(default=-1)
    filename = models.CharField(max_length=100)
    sendtime = models.DateField(auto_now=True)