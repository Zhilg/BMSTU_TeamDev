from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.hashers import make_password, check_password

# from models import UserProfiles

from django.contrib.auth import login

# Create your models here.

class UserProfiles(AbstractBaseUser):
    """
    Модель для хранения информации о пользователях.

    Attributes:
        last_login (DateTimeField): Дата и время последнего входа пользователя (автоматически обновляется).
        email (EmailField): Электронная почта пользователя (уникальное значение).
        username (CharField): Имя пользователя.
        grup (CharField): Группа пользователя.
        is_active (BooleanField): Определяет, активен ли пользователь (по умолчанию True).
        is_staff (BooleanField): Определяет, является ли пользователь сотрудником (по умолчанию False).
        is_authenticated (BooleanField): Определяет, аутентифицирован ли пользователь (по умолчанию False).

    """

    USERNAME_FIELD = 'email'
    
    def set_password(self, raw_password):
        """
        Метод для установки пароля пользователя.

        Args:
            raw_password (str): Необработанный пароль пользователя.

        """
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Метод для проверки пароля пользователя.

        Args:
            raw_password (str): Необработанный пароль, который нужно проверить.

        Returns:
            bool: True, если пароль верный, иначе False.

        """
        return check_password(raw_password, self.password)
    
    def has_perm(self, perm, obj=None):
        """
        Метод для определения, имеет ли пользователь указанные разрешения.

        Args:
            perm (str): Разрешение, которое нужно проверить.
            obj (object): Объект, для которого нужно проверить разрешение (по умолчанию None).

        Returns:
            bool: True, если пользователь имеет указанное разрешение, иначе False.

        """
        return self.is_staff

    def has_module_perms(self, app_label):
        """
        Метод для определения, имеет ли пользователь разрешения для заданного модуля.

        Args:
            app_label (str): Метка приложения.

        Returns:
            bool: True, если пользователь имеет разрешения для модуля, иначе False.

        """
        return self.is_staff    

class Tasks(models.Model):
    """
    Модель для хранения информации о заданиях.

    Attributes:
        filename (CharField): Имя файла задания (уникальное значение).
        theme (CharField): Тема задания.

    """
    filename = models.CharField(max_length=100, unique=True)
    theme = models.CharField(max_length=100)
            
class TaskPacks(models.Model):
    """
    Модель для хранения информации о пакетах заданий.

    Attributes:
        tasks (ManyToManyField): Связь с моделью Tasks.
        student (ForeignKey): Ссылка на студента, связанного с этим пакетом заданий.
        teacher (ForeignKey): Ссылка на учителя, связанного с этим пакетом заданий.
        maxgrade (IntegerField): Максимальная оценка, которую может получить студент за выполнение пакета заданий.
        mingrade (IntegerField): Минимальная оценка, которую может получить студент за выполнение пакета заданий.
        duetime (DateField): Крайний срок выполнения пакета заданий.

    """
    tasks = models.ManyToManyField(Tasks)
    student = models.ForeignKey(UserProfiles, on_delete=models.CASCADE, related_name='student_taskpacks')
    teacher = models.ForeignKey(UserProfiles, on_delete=models.CASCADE, related_name='teacher_taskpacks')
    maxgrade = models.IntegerField()
    mingrade = models.IntegerField()
    duetime = models.DateField()

class Solutions(models.Model):
    """
    Модель для хранения информации о решениях заданий.

    Attributes:
        student (ForeignKey): Ссылка на студента, связанного с этим решением.
        teacher (ForeignKey): Ссылка на учителя, связанного с этим решением.
        taskpack (ForeignKey): Ссылка на пакет заданий, к которому относится это решение.
        grade (IntegerField): Оценка за решение (по умолчанию -1).
        filename (CharField): Имя файла решения.
        sendtime (DateField): Дата и время отправки решения (автоматически обновляется).

    """
    student = models.ForeignKey(UserProfiles, on_delete=models.CASCADE, related_name='student_solutions')
    teacher = models.ForeignKey(UserProfiles, on_delete=models.CASCADE, related_name='teacher_solutions')
    taskpack = models.ForeignKey(TaskPacks, on_delete=models.CASCADE)
    grade = models.IntegerField(default=-1)
    filename = models.CharField(max_length=100)
    sendtime = models.DateField(auto_now=True)