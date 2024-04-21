from django.test import TestCase
from lms.boot import UPM


# Create your tests here.
class UserProfilesTests(TestCase):
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