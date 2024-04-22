from teamdev.BaseRep import BaseRep
from lms.models.models import *
from lms.exceptions import *

from random import choices
from datetime import date


class UserProfilesRepository(BaseRep):
    """
    Этот класс представляет собой репозиторий для управления профилями пользователей в базе данных.
    Методы:
    - get(user_id=None, email=None): Получает профили пользователей на основе user_id или email. Если предоставлен user_id, возвращает профиль пользователя с указанным id.
     Если предоставлен email, возвращает профиль пользователя с указанным email. Если не предоставлены ни user_id, ни email, возвращает все профили пользователей.
    - update(instance, validated_data): Обновляет атрибуты профиля пользователя данными, предоставленными в validated_data.
    - update_password(instance, validated_data): Обновляет пароль профиля пользователя. Требует старый пароль для подтверждения изменения.
    - insert(form, **extra_fields): Вставляет новый профиль пользователя в базу данных на основе предоставленных данных формы.
    """
    def __init__(self):
        self.model = UserProfiles

    def get(self, user_id=None, email=None):
        if user_id is not None:
            return self.model.objects.filter(pk=user_id)
        if email is not None:
            return self.model.objects.filter(email=email)
        return self.model.objects.all()

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email')
        instance.username = validated_data.get('username')
        instance.grup = validated_data.get('grup')
        instance.is_staff = validated_data.get('is_staff')

        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance

    def update_password(self, instance, validated_data):
        old = validated_data.get('old_password')
        new = validated_data.get('new_password')
        if instance.check_password(old):
            instance.set_password(new)
            instance.save()
            return instance
        else:
            raise ValueError

    def insert(self, form, **extra_fields):
        email = form['email']
        username = form['username']
        grup = form['grup']
        password = form['password']

        user = self.model(
            email=email,
            username=username,
            grup=grup,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user


class TasksRepository(BaseRep):
    """
    Этот класс представляет собой репозиторий для управления задачами в базе данных.

    Атрибуты:
    - model: Модель, представляющая задачи в базе данных.

    Методы:
    - insert(form): Вставляет новую задачу в базу данных на основе предоставленных данных формы.
    - update(form): Обновляет существующую задачу в базе данных на основе предоставленных данных формы.
    - get(filename=None, id=None): Извлекает задачи из базы данных на основе предоставленного имени файла или идентификатора.
    """
    def __init__(self):
        self.model = Tasks

    def insert(self, form):
        task = self.model(theme=form['theme'], filename=form['filename'])
        task.save()
        return task

    def update(self, form):
        pass

    def get(self, filename=None, id=None):
        if id:
            return self.model.objects.filter(id=id)
        return self.model.objects.filter(filename=filename) if filename else self.model.objects.all()


class TaskPacksRepository(BaseRep):
    """
    Этот класс представляет собой репозиторий для управления пакетами заданий в базе данных.

    Атрибуты:
    - model: Модель, представляющая пакеты заданий в базе данных.

    Методы:
    - get(teacher=None, student=None, id=None): Извлекает пакеты заданий из базы данных на основе предоставленных критериев.
    - update(form): Обновляет существующий пакет заданий в базе данных на основе предоставленных данных формы.
    - insert(form, user): Вставляет новый пакет заданий в базу данных на основе предоставленных данных формы и пользователя.
    """
    def __init__(self):
        self.model = TaskPacks

    def get(self, teacher=None, student=None, id=None):
        if teacher is not None:
            return self.model.objects.filter(teacher=teacher)
        if student is not None:
            return self.model.objects.filter(student=student)
        if id is not None:
            return self.model.objects.filter(pk=id)
        else:
            return self.model.objects.all()

    def update(self, form):
        pass

    def insert(self, form, user):
        N = form['n']
        if N <= 0:
            raise NonPositiveNException

        maxgrade, mingrade = form['maxgrade'], form['mingrade']
        if maxgrade < 0 or mingrade < 0 or maxgrade < mingrade:
            raise WrongGrades

        student_ids = UserProfiles.objects.filter(grup=form['group'])  # Все id студентов какой-то группы
        if not student_ids.__len__():
            raise NoSuchGroupException

        duetime = form['duetime']
        if duetime < date.today():
            raise WrongDeadlineException

        tasks_ids = list(TasksRepository().model.objects.filter(theme=form['theme']).values_list('id',
                                                                                                 flat=True))  # Все id заданий на соотв тему
        len = tasks_ids.__len__()
        if len == 0:
            raise NoSuchThemeException

        elif len < N:
            raise NotEnoughTasksException

        teacher = user

        ret_list = []

        for student in student_ids:
            pack = self.model(student=student, teacher=teacher, duetime=duetime, maxgrade=maxgrade, mingrade=mingrade)
            pack.save()
            ret_list.append(pack)
            pack.tasks.add(*choices(tasks_ids, k=form['n']))

        return ret_list


class SolutionsRepository(BaseRep):
    '''
    Этот класс представляет собой репозиторий для управления решениями в базе данных.

    Атрибуты:
    - model: Модель, представляющая решения задач в базе данных.

    Методы:
    - get(teacher=None, student=None, id=None): Извлекает решения задач из базы данных на основе предоставленных критериев.
    - insert(form, user): Вставляет новое решение задачи в базу данных на основе предоставленных данных формы и пользователя.
    - update(form, instance): Обновляет существующее решение задачи в базе данных на основе предоставленных данных формы и экземпляра решения.

    '''
    def __init__(self) -> None:
        self.model = Solutions

    def get(self, teacher=None, student=None, id=None):
        if id:
            return self.model.objects.filter(id=id)
        if teacher is not None:
            return self.model.objects.filter(teacher=teacher)
        if student is not None:
            return self.model.objects.filter(student=student)
        return self.model.objects.all()

    def insert(self, form, user):
        taskpacksid = form['taskpackid']
        filename = form['filename']

        query = self.model.objects.filter(filename=filename)
        if query.__len__():
            raise FileAlreadyExists

        query = TaskPacksRepository().get(id=taskpacksid)
        if not query.__len__():
            raise NoSuchTaskPacks

        query = TaskPacksRepository().get(student=user).values_list('id', flat=True)

        if taskpacksid not in list(query):
            raise WrongTaskPackID

        taskpack = TaskPacksRepository().get(id=taskpacksid).first()
        teacher = taskpack.teacher
        solution = self.model(filename=filename, taskpack=taskpack, student=user, teacher=teacher)
        solution.save()
        return solution

    def update(self, form, instance):
        instance.grade = form['grade']
        instance.save()
        return instance
 