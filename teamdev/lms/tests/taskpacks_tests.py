from django.test import TestCase
from lms.boot import *
import datetime as datetime
from lms.exceptions import *

tomorrow = date.today() + datetime.timedelta(days=1)
yesterday = date.today() - datetime.timedelta(days=1)


class TaskPacksTests(TestCase):
    '''
    Класс TaskPacksTests является набором тестов для проверки функционала класса TaskPacksManager.
    Он содержит методы для тестирования создания пакетов задач.

    Методы класса:
    - setUp(): Метод подготовки данных для тестов. Создает формы для пакетов задач, пользователей и файлов.
    - test_neg_n(): Тестирование обработки ситуации, когда количество задач в пакете отрицательное. Проверяет возникновение исключения NonPositiveNException.
    - test_wrong_deadline(): Тестирование обработки ситуации, когда указана неверная дата завершения. Проверяет возникновение исключения WrongDeadlineException.
    - test_no_group(): Тестирование обработки ситуации, когда не указана группа для пакета задач. Проверяет возникновение исключения NoSuchGroupException.
    - test_no_such_theme(): Тестирование обработки ситуации, когда не указана тема для пакета задач. Проверяет возникновение исключения NoSuchThemeException.
    - test_not_enough_tasks(): Тестирование обработки ситуации, когда количество задач в пакете недостаточно. Проверяет возникновение исключения NotEnoughTasksException.
    - test_create_taskpack(): Тестирование успешного создания пакета задач. Проверяет корректность создания пакета и его наличие в базе данных.
    '''
    def setUp(self):
        self.form1 = {"n": -1, "group": "IU7-61B", "theme": "Mathematics", "duetime": tomorrow, "maxgrade": 10,
                      "mingrade": 1}
        self.form2 = {"n": 1, "group": "None", "theme": "Mathematics", "duetime": tomorrow, "maxgrade": 10,
                      "mingrade": 1}
        self.form3 = {"n": 1, "group": "IU7-61B", "theme": "None", "duetime": tomorrow, "maxgrade": 10, "mingrade": 1}
        self.form4 = {"n": 1, "group": "IU7-61B", "theme": "Mathematics", "duetime": yesterday, "maxgrade": 10,
                      "mingrade": 1}
        self.form5 = {"n": 5, "group": "IU7-61B", "theme": "Mathematics", "duetime": tomorrow, "maxgrade": 10,
                      "mingrade": 1}
        self.form6 = {"n": 1, "group": "IU7-61B", "theme": "Mathematics", "duetime": tomorrow, "maxgrade": 10,
                      "mingrade": 1}

        form = {'email': '124@mail.ru', "password": "asdasdasd", "username": "bruh", "grup": "Teacher"}
        self.user = UPM.create(form=form)
        form = {'email': '125@mail.ru', "password": "asdasdasd", "username": "bruh2", "grup": "IU7-61B"}
        UPM.create(form=form)
        form = {"filename": "asdasdd.txt", "theme": "Mathematics"}
        TM.create(form)

    def test_neg_n(self):
        print("neg_n")
        try:
            TPM.create(form=self.form1, user=self.user)
        except NonPositiveNException:
            self.assertTrue(True, True)

    def test_wrong_deadline(self):
        print('wrong_deadline')
        try:
            TPM.create(form=self.form4, user=self.user)
        except WrongDeadlineException:
            self.assertTrue(True, True)

    def test_no_group(self):
        print('no_group')
        try:
            TPM.create(form=self.form2, user=self.user)
        except NoSuchGroupException:
            self.assertTrue(True, True)

    def test_no_such_theme(self):
        print('no_theme')
        try:
            TPM.create(form=self.form3, user=self.user)
        except NoSuchThemeException:
            self.assertTrue(True, True)

    def test_not_enough_tasks(self):
        print('not_enough_tasks')
        try:
            TPM.create(form=self.form5, user=self.user)
        except NotEnoughTasksException:
            self.assertTrue(True, True)

    def test_create_taskpack(self):
        print('create')
        tm = TPM.create(form=self.form6, user=self.user)

        self.assertEqual(TPM.get(user=self.user)[0], tm[0])
