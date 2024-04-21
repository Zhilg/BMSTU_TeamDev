from django.test import TestCase
from lms.tests.builder import *
from lms.exceptions import *
from datetime import date
from unittest.mock import MagicMock


class SolutionsTests(TestCase):
    def setUp(self):
        self.user = UserBuilder.create_student()
        self.another_user = UserBuilder.create_student2()

        self.taskpack = TaskPackBuilder.create()

        self.test_form_1 = {"filename": "a.txt", "taskpackid": self.taskpack[0].id}

        self.test_form_5 = {"filename": "a2.txt", "taskpackid": self.taskpack[0].id}
        self.test_form_2 = {"filename": "d.txt", "taskpackid": self.taskpack[0].id}
        self.test_form_3 = {"filename": "b.txt", "taskpackid": 1000}
        self.test_form_4 = {"filename": "c.txt", "taskpackid": self.taskpack[0].id}

    def test_create_solution(self):
        print('create_solution')
        solution = SM.create(self.user, self.test_form_1)
        self.assertIsInstance(solution, SM.rep.model)

    def test_create_solution_mock_london(self):
        testSM = SolutionsManager()
        teacher = UserBuilder.create_teacher2()
        exp_res = Solutions(filename=self.test_form_5['filename'], taskpack=self.taskpack[0], student=self.user,
                            teacher=teacher)
        testSM.create = MagicMock(return_value=exp_res)
        result = testSM.create(form=self.test_form_5, user=teacher)
        self.assertEqual(exp_res, result)

    def test_file_exists(self):
        print('file_already_exists')
        SM.create(self.user, self.test_form_2)
        with self.assertRaises(FileAlreadyExists):
            SM.create(self.user, self.test_form_2)

    def test_no_taskpack(self):
        print('no_taskpack')
        with self.assertRaises(NoSuchTaskPacks):
            SM.create(self.user, self.test_form_3)

    def test_wrong_taskpack(self):
        print('wrong_taskpack')
        with self.assertRaises(WrongTaskPackID):
            SM.create(self.another_user, self.test_form_4)