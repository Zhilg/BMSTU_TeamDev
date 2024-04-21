from django.test import TestCase
from lms.boot import *
import datetime as datetime
from lms.exceptions import *

tomorrow = date.today() + datetime.timedelta(days=1)
yesterday = date.today() - datetime.timedelta(days=1)


class TaskPacksTests(TestCase):
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
