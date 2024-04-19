from lms.repositories.repositories import *
from bd_course.BaseManag import BaseUserManag, BaseManag

from lms.exceptions import *
from django.contrib.auth.models import BaseUserManager

class UserProfilesManager(BaseUserManag, BaseUserManager):
    """
    Менеджер профилей пользователей, обеспечивающий операции создания, получения и обновления пользовательских профилей.
    """

    def __init__(self):
        """
        Инициализация менеджера профилей пользователей.
        """
        super().__init__()
        self.rep = None

    def create(self, form, **extra_fields):
        """
        Создает новый пользовательский профиль на основе данных из формы.

        Параметры:
        - form (dict): Словарь с данными формы для создания профиля.
        - extra_fields: Дополнительные поля профиля.

        Возвращает:
        - Созданный пользовательский профиль.
        
        Исключения:
        - ValueError: В случае, если пользователь с указанным адресом электронной почты уже существует.
        """
        if self.get(email=form['email']):
            raise ValueError
        user = self.rep.insert(form, **extra_fields)
        return user

    def create_superuser(self, email, username, grup, password=None, **extra_fields):
        """
        Создает нового суперпользователя с правами администратора.

        Параметры:
        - email (str): Адрес электронной почты суперпользователя.
        - username (str): Имя пользователя суперпользователя.
        - grup: Группа пользователя.
        - password (str): Пароль для суперпользователя.
        - extra_fields: Дополнительные поля профиля суперпользователя.

        Возвращает:
        - Созданный суперпользователь.
        
        Исключения:
        - ValueError: Если не указаны обязательные параметры для создания суперпользователя.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.rep.insert(email, username, grup, password, **extra_fields)
    
    def get(self, id=None, email=None):
        """
        Получает пользователя по его идентификатору или адресу электронной почты.

        Параметры:
        - id (int): Идентификатор пользователя.
        - email (str): Адрес электронной почты пользователя.

        Возвращает:
        - Найденный пользователь.
        
        Исключения:
        - DoesNotExist: Если пользователь с указанными параметрами не найден.
        """
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
        """
        Аутентифицирует пользователя на основе предоставленных адреса электронной почты и пароля.

        Параметры:
        - email (str): Адрес электронной почты пользователя.
        - password (str): Пароль пользователя.
        - request: Объект запроса.

        Возвращает:
        - Аутентифицированного пользователя.
        
        Исключения:
        - ValueError: Если пользователь с указанным адресом электронной почты не найден или пароль неверен.
        - KeyError: Если пользователь неактивен.
        """
        email = self.normalize_email(email)
        user = self.get(email=email)[0]
        if user is None:
            raise ValueError
        if not user.is_active:
            raise KeyError
        if user.check_password(password):
            login(request, user, backend="lms.backends.EmailBackend")
            return user
        else:
            raise ValueError
    
    def update(self, instance, validated_data):
        """
        Обновляет данные профиля пользователя.

        Параметры:
        - instance: Экземпляр профиля пользователя.
        - validated_data: Проверенные данные для обновления.

        Возвращает:
        - Обновленный профиль пользователя.
        """
        return self.rep.update(instance, validated_data)
        
    def change_password(self, instance, validated_data):
        """
        Изменяет пароль пользователя.

        Параметры:
        - instance: Экземпляр профиля пользователя.
        - validated_data: Проверенные данные для изменения пароля.

        Возвращает:
        - Обновленный профиль пользователя с измененным паролем.
        """
        return self.rep.update_password(instance, validated_data)