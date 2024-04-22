from django.test import TestCase
from lms.boot import UPM


# Create your tests here.
class UserProfilesTests(TestCase):
    '''
    Класс UserProfilesTests является набором тестов для проверки функционала класса UserProfilesManager.
    Он содержит методы для тестирования создания, получения и изменения профилей пользователей.

    Методы класса:
    - setUp(): Метод подготовки данных для тестов. Создает пользователя с указанными данными: email, пароль, имя пользователя и группа.
    - test_create(): Тестирование успешного создания профиля пользователя. Проверяет, что созданный профиль соответствует модели UserProfilesManager.
    - test_get(): Тестирование получения профиля пользователя по email. Проверяет, что полученный профиль соответствует модели UserProfilesManager.
    - test_ch_pas(): Тестирование изменения пароля пользователя. Проверяет, что пароль пользователя успешно изменен на новый и соответствует ожидаемому значению.
    '''
    def setUp(self):
        form = {'email': '124@mail.ru', "password": "asdasdasd", "username": "bruh", "grup": "Teacher"}
        self.user = UPM.create(form=form)

    def test_create(self):
        print('create')
        self.assertIsInstance(self.user, UPM.rep.model)

    def test_get(self):
        ('get')
        prof = UPM.get(email='124@mail.ru')[0]
        self.assertIsInstance(prof, UPM.rep.model)

    def test_ch_pas(self):
        ('change_password')
        form = {"old_password": "asdasdasd", "new_password": "12345678"}
        prof = UPM.get(email='124@mail.ru')[0]
        UPM.change_password(prof, form)
        self.assertTrue(prof.check_password(form["new_password"]))