from lms.repositories.repositories import *
from teamdev.BaseManag import BaseUserManag, BaseManag

from lms.exceptions import *
from django.contrib.auth.models import BaseUserManager


# для менеджеров свои модельки, а репозиторий конвертирует из модели в бд в модель для менеджеров
# модели в ОРМ слишком сильно связаны с менеджерами, ослабить эту связь, абстрагироваться
# создавать менеджеров через какойто конструктор, отдельный класс (фабрику), туда передавать связь с репозиторием


class UserProfilesManager(BaseUserManag, BaseUserManager):
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