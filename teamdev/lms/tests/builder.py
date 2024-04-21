from lms.boot import *


class UserBuilder():
    def create_teacher():
        form = {'email': '124@mail.ru', "password": "asdasdasd", "username": "bruh", "grup": "Teacher"}
        return UPM.create(form)

    def create_teacher2():
        form = {'email': '128@mail.ru', "password": "asdasdasd", "username": "bruh", "grup": "Teacher"}
        return UPM.create(form)

    def create_student():
        form = {'email': '125@mail.ru', "password": "asdasdasd", "username": "bruh2", "grup": "IU7-61B"}
        return UPM.create(form)

    def create_student2():
        form = {'email': '126@mail.ru', "password": "asdasdasd", "username": "bruh2", "grup": "IU7-71B"}
        return UPM.create(form=form)


class TaskBuilder():
    def create():
        form = {"filename": "asdasdd.txt", "theme": "Mathematics"}
        return TM.create(form)


class TaskPackBuilder():
    def create():
        TaskBuilder.create()
        form = {"n": 1, "group": "IU7-61B", "theme": "Mathematics", "duetime": date.today(), 'maxgrade': 10,
                "mingrade": 1}
        return TPM.create(form, user=UserBuilder.create_teacher())
