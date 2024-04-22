from lms.repositories.repositories import *
from teamdev.BaseManag import BaseUserManag, BaseManag

from lms.exceptions import *
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import login



# для менеджеров свои модельки, а репозиторий конвертирует из модели в бд в модель для менеджеров
# модели в ОРМ слишком сильно связаны с менеджерами, ослабить эту связь, абстрагироваться
# создавать менеджеров через какойто конструктор, отдельный класс (фабрику), туда передавать связь с репозиторием


class UserProfilesManager(BaseUserManag, BaseUserManager):
    '''
    Класс UserProfilesManager является менеджером пользователей, предназначенным для работы с пользователями в системе.

    Методы класса:
    - create(form, **extra_fields): Создает нового пользователя на основе переданных данных из формы.
    Проверяет уникальность email пользователя и вызывает метод insert у репозитория для сохранения пользователя.
    - create_superuser(email, username, grup, password=None, **extra_fields): Создает суперпользователя с дополнительными правами.
    Проверяет и устанавливает флаги is_staff и is_superuser. Вызывает метод insert у репозитория для сохранения суперпользователя.
    - get(id=None, email=None): Получает пользователя по id или email. Если пользователь не найден, возвращает None.
    - auth_user(email, password, request): Аутентифицирует пользователя по email и паролю.
    Проверяет активность пользователя и сравнивает пароль. При успешной аутентификации вызывает функцию login и возвращает пользователя.
    - update(instance, validated_data): Обновляет данные пользователя на основе переданных данных.
    Вызывает метод update у репозитория для обновления информации о пользователе.
    - change_password(instance, validated_data): Изменяет пароль пользователя на основе переданных данных.
    Вызывает метод update_password у репозитория для изменения пароля.

    Атрибуты класса:
    - rep: Репозиторий для работы с данными пользователей.

    '''
    def __init__(self):
        super().__init__()
        self.rep = None

    def create(self, form, **extra_fields):

        if self.get(email=form['email']):
            raise ValueError
        user = self.rep.insert(form, **extra_fields)
        return user

    def create_superuser(self, email, username, grup, password=None,
                         **extra_fields):  # зависимость передавать через конструктор
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.rep.insert(email, username, grup, password, **extra_fields)

    def get(self, id=None, email=None):
        if id:
            try:
                return self.rep.get(user_id=id)
            except self.rep.model.DoesNotExist:
                return None
        if email:
            try:
                return self.rep.get(email=email)
            except self.rep.model.DoesNotExist:
                return None

        return self.rep.get()

    def auth_user(self, email, password, request):
        email = self.normalize_email(email)
        user = self.get(email=email)[0]
        if user is None:
            return ValueError
        if not user.is_active:
            raise KeyError
        if user.check_password(password):
            login(request, user, backend="lms.backends.EmailBackend")
            return user
        else:
            raise ValueError

    def update(self, instance, validated_data):
        return self.rep.update(instance, validated_data)

    def change_password(self, instance, validated_data):
        return self.rep.update_password(instance, validated_data)


class TasksManager(BaseManag, models.Model):
    '''
    Класс TasksManager является менеджером задач и предназначен для работы с задачами в системе.

    Методы класса:
    - create(form): Создает новую задачу на основе переданных данных из формы. Проверяет, существует ли уже задача с таким же именем файла (filename). Если задача уже существует, вызывается исключение FileAlreadyExists. В противном случае, задача добавляется в хранилище данных.
    - get(filename=None, id=None): Получает задачу по имени файла (filename) или по идентификатору (id). Возвращает найденную задачу.
    - delete(filename): Удаляет задачу из хранилища данных по имени файла (filename).

    Атрибуты класса:
    - rep: Репозиторий для работы с данными задач.

    Исключения:
    - FileAlreadyExists: Исключение, которое возникает при попытке создать задачу с именем файла, которое уже существует в системе.
    '''
    def __init__(self):
        super().__init__()

    def create(self, form):
        query = self.rep.get(form['filename'])
        if query.__len__():
            raise FileAlreadyExists
        return self.rep.insert(form)

    def get(self, filename=None, id=None):
        query = self.rep.get(filename, id)
        return query

    def delete(self, filename):
        file = self.rep.get(filename)
        file.delete()


class TaskPacksManager(BaseManag, models.Model):
    '''
    Класс TaskPacksManager является менеджером пакетов задач и предназначен для работы с пакетами задач в системе.

    Методы класса:
    - create(form, user): Создает новый пакет задач на основе переданных данных из формы и пользователя, который создает пакет. Добавляет новый пакет в хранилище данных.
    - get(user=None, id=None): Получает пакет задач по пользователю (user) или по идентификатору (id). Возвращает найденный пакет задач.
    - unpack_fields_values(user): Получает значения полей пакетов задач для конкретного пользователя. Возвращает список значений полей пакетов задач.
    - get_meta_fields(): Получает метаданные полей модели пакетов задач. Возвращает список имен полей модели, за исключением первого и последнего поля.

    Атрибуты класса:
    - rep: Репозиторий для работы с данными пакетов задач.
    '''
    def __init__(self):
        super().__init__()

    def create(self, form, user):
        return self.rep.insert(form, user)

    def get(self, user=None, id=None):
        if id:
            return self.rep.get(id=id)
        if not user:
            return self.rep.get()
        if user.grup == 'Teacher':
            TASKPACKS_QUERY = self.rep.get(teacher=user.id)
        else:
            TASKPACKS_QUERY = self.rep.get(student=user.id)
        return TASKPACKS_QUERY

    def unpack_fields_values(self, user):
        TASKPACKS_QUERY = self.get(user)
        return [list(i.values()) for i in TASKPACKS_QUERY]

    def get_meta_fields(self):
        return [f.name for f in self.rep.model._meta.get_fields()[1:-1]]


class SolutionsManager(BaseManag, models.Model):
    '''
    Класс SolutionsManager является менеджером решений и предназначен для работы с решениями задач в системе.

    Методы класса:
    - create(user, form): Создает новое решение задачи на основе переданных данных из формы и пользователя, который создает решение.
    Добавляет новое решение в хранилище данных.
    - update(form, instance): Обновляет существующее решение задачи на основе переданных данных из формы и экземпляра решения.
    Возвращает обновленное решение.
    - get(user=None, id=None): Получает решение задачи по пользователю (user) или по идентификатору (id).
    Возвращает найденное решение задачи.
    - get_meta_fields(): Получает метаданные полей модели решений задач. Возвращает список имен полей модели.
    - unpack_fields_values(user): Получает значения полей решений задач для конкретного пользователя.
    Возвращает список значений полей решений задач.

    Атрибуты класса:
    - rep: Репозиторий для работы с данными решений задач.
    '''
    def __init__(self):
        super().__init__()

    def create(self, user, form):
        return self.rep.insert(form, user)

    def update(self, form, instance):
        return self.rep.update(form, instance)

    def get(self, user=None, id=None):
        if id:
            return self.rep.get(id=id)
        if user:
            if user.grup == 'Teacher':
                SOLUTIONS_QUERY = self.rep.get(teacher=user.id)
            else:
                SOLUTIONS_QUERY = self.rep.get(student=user.id)
            return SOLUTIONS_QUERY
        return self.rep.get()

    def get_meta_fields(self):
        return [f.name for f in self.rep.model._meta.get_fields()]

    def unpack_fields_values(self, user):
        query = self.get(user)
        return [list(i.values()) for i in query]
