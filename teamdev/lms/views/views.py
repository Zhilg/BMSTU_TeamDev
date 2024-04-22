from lms.forms.forms import *
from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse

from django.contrib.auth.models import AnonymousUser

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import status
from rest_framework.response import Response
from lms.responses import *
from django.contrib.auth import logout
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from lms.serials.sers import UserProfilesSerializer, UserAuthSerializer, TasksSerializer, TaskPacksSerializer, TaskPacksModelSerializer, SolutionsModelSerializer, SolutionsSerializer

from lms.boot import *

class TasksView(APIView):
    '''
    Класс TasksView представляет собой API для работы с задачами.
    Он содержит два метода: post для создания новой задачи и get для получения списка всех задач.

    Метод post:
    - Проверяет, авторизован ли пользователь. Если нет, возвращает статус 401 UNAUTHORIZED.
    - Проверяет, является ли пользователь персоналом или принадлежит ли к группе "Teacher". Если нет, возвращает статус 403 FORBIDDEN.
    - Принимает данные о задаче в формате JSON: filename (имя файла) и theme (тема задачи).
    - Сохраняет задачу с помощью сериализатора TasksSerializer.
    - Возвращает успешный ответ с кодом 201 CREATED, сообщением "Successful operation" и заголовком Location, указывающим на URL созданной задачи.

    Метод get:
    - Проверяет, авторизован ли пользователь. Если нет, возвращает статус 401 UNAUTHORIZED.
    - Получает список всех задач с помощью метода TM.get().
    - Сериализует список задач с помощью TasksSerializer.
    - Возвращает список задач в формате JSON с кодом 200 OK.
    '''
    @swagger_auto_schema(responses={201: "created", 401:"unauthorized", 403:"Not permitted", 500:'failed'},
                    request_body=openapi.Schema
                    (
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "filename":openapi.Schema(
                                type=openapi.TYPE_STRING,
                                example='maths100.txt'
                            ),
                            "theme":openapi.Schema(
                                type=openapi.TYPE_STRING,
                                example='maths'
                            )
                        },
                        required=["filename", "theme"]
                    ))
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if not request.user.is_staff and not request.user.grup != "Teacher":
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = TasksSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            response_data = {'message': 'Successful operation'}
            response_headers = {'Location': f'http://localhost:8000/tasks/{task.id}'}
            return Response(status=status.HTTP_201_CREATED, data=response_data, headers=response_headers)

 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(responses={200: "success", 401:"unauthorized", 500:'failed'})
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        tasks = TM.get()
        serializer = TasksSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskPacksView(APIView):
    '''
    Класс TaskPacksView представляет собой API для работы с комплектами задач.
    Он содержит два метода: post для создания нового комплекта задач и get для получения списка всех комплектов.

    Метод post:
    - Проверяет, авторизован ли пользователь. Если нет, возвращает статус 401 UNAUTHORIZED.
    - Проверяет, является ли пользователь персоналом или принадлежит ли к группе "Teacher". Если нет, возвращает статус 403 FORBIDDEN.
    - Принимает данные о комплекте задач в формате JSON: n (количество задач), duetime (дата дедлайна),
    theme (тема комплекта), group (группа), maxgrade (максимальная оценка), mingrade (минимальная оценка).
    - Сохраняет комплект задач с помощью сериализатора TaskPacksSerializer.
    - Возвращает успешный ответ с кодом 201 CREATED и сообщением "Successful operation". О
    брабатывает возможные исключения и возвращает соответствующие сообщения об ошибке.

    Метод get:
    - Проверяет, авторизован ли пользователь. Если нет, возвращает статус 401 UNAUTHORIZED.
    - Получает список всех комплектов задач с помощью метода TPM.get().
    - Сериализует список комплектов задач с помощью TaskPacksModelSerializer.
    - Возвращает список комплектов задач в формате JSON с кодом 200 OK.
    '''
    @swagger_auto_schema(
        responses={201: "created", 400: "bad request", 401: "unauthorized", 403: "Not permitted", 500: 'failed'},
        request_body=openapi.Schema
            (
            type=openapi.TYPE_OBJECT,
            properties={
                "n": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    example=1
                ),
                "duetime": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example='2023-12-29'
                ),
                "theme": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example='maths'
                ),
                'group': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example='IU7-71B'
                ),
                "maxgrade": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    example=10
                ),
                "mingrade": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    example=0
                )
            },

            required=["n", "duetime", "theme", "group", "maxgrade", "mingrade"]
        ))
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if not request.user.is_staff and not request.user.grup != "Teacher":
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = TaskPacksSerializer(data=request.data, partial=True, context={"user": request.user})
        if serializer.is_valid():
            try:
                taskpack = serializer.save()

                response_data = {'message': 'Successful operation'}
                return Response(status=status.HTTP_201_CREATED, data=response_data)

            except NonPositiveNException:
                return Response({"message": 'Количество заданий в комплекте не может быть <= 0'},
                                status=status.HTTP_400_BAD_REQUEST)
            except WrongGrades:
                return Response({"message": 'Неправильные границы оценки'}, status=status.HTTP_400_BAD_REQUEST)
            except NoSuchGroupException:
                return Response({"message": 'Такой группы нет в системе'}, status=status.HTTP_400_BAD_REQUEST)
            except WrongDeadlineException:
                return Response({"message": "Неправильный дедлайн данных комплектов"},
                                status=status.HTTP_400_BAD_REQUEST)
            except NoSuchThemeException:
                return Response({"message": 'Заданий с такой темой нет в системе'}, status=status.HTTP_400_BAD_REQUEST)
            except NotEnoughTasksException:
                return Response({"message": 'Недостаточно заданий в системе для формирования комплекта'},
                                status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: "success", 401: "unauthorized", 500: 'failed'})
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        taskpacks = TPM.get()
        serializer = TaskPacksModelSerializer(taskpacks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SingleTaskPackView(APIView):
    '''
    Класс SingleTaskPackView представляет собой API для работы с отдельным комплектом задач по его идентификатору (id).
    Он содержит два метода: get для получения информации о комплекте задач и delete для удаления комплекта задач.

    Метод get:
    - Проверяет, авторизован ли пользователь. Если нет, возвращает статус 401 UNAUTHORIZED.
    - Проверяет, передан ли корректный идентификатор комплекта задач. Если нет, возвращает статус 400 BAD REQUEST.
    - Получает комплект задач по указанному идентификатору с помощью метода TPM.get(id=id).
    - Если комплект задач не найден, возвращает статус 404 NOT FOUND.
    - Сериализует информацию о комплекте задач с помощью TaskPacksModelSerializer и возвращает её в формате JSON с кодом 200 OK.

    Метод delete:
    - Проверяет, авторизован ли пользователь. Если нет, возвращает статус 401 UNAUTHORIZED.
    - Проверяет, является ли пользователь персоналом или принадлежит ли к группе "Teacher". Если нет, возвращает статус 403 FORBIDDEN.
    - Проверяет, передан ли корректный идентификатор комплекта задач. Если нет, возвращает статус 400 BAD REQUEST.
    - Получает комплект задач по указанному идентификатору с помощью метода TPM.get(id=id).
    - Если комплект задач не найден, возвращает статус 404 NOT FOUND.
    - Удаляет комплект задач и возвращает статус 204 NO CONTENT.
    '''
    @swagger_auto_schema(responses={200: "success", 401: "unauthorized", 404: "Not found", 500: 'failed'})
    def get(self, request, id):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if id is None or id < 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        taskpack = TPM.get(id=id)
        if not taskpack:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TaskPacksModelSerializer(taskpack[0])
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={200: "success", 401: "unauthorized", 403: "Not permitted", 404: "Not found", 500: 'failed'})
    def delete(self, request, id):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if not request.user.is_staff and not request.user.grup != "Teacher":
            return Response(status=status.HTTP_403_FORBIDDEN)
        if id is None or id < 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        task = TPM.get(id=id)
        if task is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SolutionsView(APIView):
    '''
    Класс SolutionsView представляет собой API для работы с решениями задач.
    Он содержит два метода: post для создания нового решения и get для получения списка всех решений.

    Метод post:
    - Проверяет, авторизован ли пользователь. Если нет, возвращает статус 401 UNAUTHORIZED.
    - Принимает данные запроса, включающие идентификатор комплекта задач (taskpackid) и название файла (filename).
    - Создает сериализатор SolutionsSerializer с переданными данными и контекстом пользователя.
    - Если данные валидны, сохраняет решение и возвращает сообщение об успешной операции с кодом 201 CREATED.
    - Если файл с таким названием уже существует, возвращает статус 400 BAD REQUEST.
    - Если указанный комплект задач не существует, возвращает статус 404 NOT FOUND.
    - Если комплект задач не принадлежит пользователю, возвращает статус 400 BAD REQUEST.

    Метод get:
    - Проверяет, авторизован ли пользователь. Если нет, возвращает статус 401 UNAUTHORIZED.
    - Получает список всех решений задач с помощью метода SM.get().
    - Сериализует список решений с помощью SolutionsModelSerializer и возвращает его в формате JSON с кодом 200 OK.
    '''
    @swagger_auto_schema(responses={201: "created", 400: "bad request", 401: "unauthorized", 500: 'failed'},
                         request_body=openapi.Schema
                             (
                             type=openapi.TYPE_OBJECT,
                             properties={
                                 "taskpackid": openapi.Schema(
                                     type=openapi.TYPE_INTEGER,
                                     example=1
                                 ),
                                 "filename": openapi.Schema(
                                     type=openapi.TYPE_STRING,
                                     example='solution1000.txt'
                                 ),
                             },

                             required=["taskpackid", "filename"]
                         ))
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = SolutionsSerializer(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            try:
                sol = serializer.save()
                response_data = {'message': 'Successful operation'}
                response_headers = {'Location': f'http://localhost:8000/solutions/{sol.id}'}
                return Response(status=status.HTTP_201_CREATED, data=response_data, headers=response_headers)
            except FileAlreadyExists:
                return Response({"message": "Файл с таким названием уже существует в системе"},
                                status=status.HTTP_400_BAD_REQUEST)
            except NoSuchTaskPacks:
                return Response({"message": "Данного комплекта заданий не существует"},
                                status=status.HTTP_404_NOT_FOUND)
            except WrongTaskPackID:
                return Response({"message": "Данный комплект заданий не ваш"}, status=status.HTTP_400_BAD_REQUEST)



        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: "success", 401: "unauthorized", 500: 'failed'})
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        solutio = SM.get()
        serializer = SolutionsModelSerializer(solutio, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SingleSolutionView(APIView):
    '''
    Класс SingleSolutionView представляет собой APIView для работы с отдельным решением задачи.
    Он содержит три метода: get для получения конкретного решения, delete для удаления решения и patch для обновления информации о решении.

    Метод get:
    - Проверяет, авторизован ли пользователь. Если нет, возвращает статус 401 UNAUTHORIZED.
    - Принимает идентификатор решения (id) в качестве параметра.
    - Если id не передан или меньше нуля, возвращает статус 400 BAD REQUEST.
    - Получает решение по указанному id с помощью метода SM.get().
    - Если решение не найдено, возвращает статус 404 NOT FOUND.
    - Сериализует найденное решение с помощью SolutionsModelSerializer и возвращает его в формате JSON с кодом 200 OK.

    Метод delete:
    - Проверяет, авторизован ли пользователь. Если нет, возвращает статус 401 UNAUTHORIZED.
    - Принимает идентификатор решения (id) в качестве параметра.
    - Если id не передан или меньше нуля, возвращает статус 400 BAD REQUEST.
    - Получает решение по указанному id с помощью метода SM.get().
    - Если решение не найдено, возвращает статус 404 NOT FOUND.
    - Удаляет найденное решение и возвращает статус 204 NO CONTENT.

    Метод patch:
    - Проверяет, авторизован ли пользователь. Если нет, возвращает статус 401 UNAUTHORIZED.
    - Проверяет, является ли пользователь учеником или преподавателем. Если нет, возвращает статус 403 FORBIDDEN.
    - Принимает идентификатор решения (id) в качестве параметра.
    - Если id не передан или меньше нуля, возвращает статус 400 BAD REQUEST.
    - Получает решение по указанному id с помощью метода SM.get().
    - Если решение не найдено, возвращает статус 404 NOT FOUND.
    - Обновляет информацию о решении на основе переданных данных и возвращает обновленное решение с кодом 204 NO CONTENT в случае успешного обновления.
    - В случае невалидных данных возвращает статус 400 BAD REQUEST.
    '''
    @swagger_auto_schema(responses={200: "success", 401: "unauthorized", 404: "Not found", 500: 'failed'})
    def get(self, request, id):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if id is None or id < 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        sol = SM.get(id=id)
        if not sol:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SolutionsModelSerializer(sol[0])
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={204: "success", 401: "unauthorized", 404: "Not found", 500: 'failed'})
    def delete(self, request, id):

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if id is None or id < 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        sol = SM.get(id=id)
        if sol is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        sol.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        responses={201: "created", 400: "bad request", 401: "unauthorized", 403: "Not permitted", 500: 'failed'},
        request_body=openapi.Schema
            (
            type=openapi.TYPE_OBJECT,
            properties={
                "grade": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    example=10
                )
            },

            required=["grade"]
        ))
    def patch(self, request, id):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if not request.user.is_staff and not request.user.grup != "Teacher":
            return Response(status=status.HTTP_403_FORBIDDEN)
        if id is None or id < 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        sol = SM.get(id=id)[0]
        if not sol:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SolutionsModelSerializer(sol, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update()
            return Response(serializer.validated_data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    '''
    Класс UserLoginView представляет собой API для входа пользователя в систему.
    Он содержит один метод post для обработки запроса на аутентификацию пользователя.

    Метод post:
    - Принимает запрос с данными в формате JSON, содержащими email и password.
    - Проверяет валидность данных с помощью сериализатора UserAuthSerializer.
    - Если данные валидны, извлекает пользователя из сериализатора и возвращает сообщение "Успешный вход в систему" с кодом 200 OK.
    - Если данные неверны или не прошли валидацию, возвращает ошибки сериализатора с кодом 400 BAD REQUEST.
    '''
    @swagger_auto_schema(responses={201: "created", 400:"bad request", 401:"invalid login or password", 500:'failed'},
                        request_body=openapi.Schema
                        (
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "email":openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example='email@domain.com'
                                ),
                                "password":openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example='password'
                                )
                            },
                            required=['email', 'password']
                        ))
    def post(self, request):        
        serializer = UserAuthSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response({'message': 'Успешный вход в систему.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class UserRegisterView(APIView):
    '''
    Класс UserRegisterView представляет собой API для регистрации нового пользователя в системе.
    Он содержит один метод post для обработки запроса на создание нового пользователя.

    Метод post:
    - Принимает запрос с данными в формате JSON, содержащими email, password, username и grup.
    - Проверяет валидность данных с помощью сериализатора UserProfilesSerializer.
    - Если данные валидны, создает новый профиль пользователя и возвращает сообщение "Успешная операция" с кодом
    201 CREATED и заголовок Location с ссылкой на созданный профиль пользователя.
    - Если данные неверны или не прошли валидацию, возвращает ошибки сериализатора с кодом 400 BAD REQUEST.
    '''
    @swagger_auto_schema(responses={201: "created", 400:"bad request", 500:'failed'},
                        request_body=openapi.Schema
                        (
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "email":openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example='email100@domain.com'
                                ),
                                "password":openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example='password'
                                ),
                                "username" : openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example='V.V.Putin'
                                ),
                                "grup" : openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example='IU7-71B'
                                )
                            },
                            required=['email', 'password', "username", "grup"]
                        ))
    def post(self, request):
        
        serializer = UserProfilesSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            user_profile = serializer.save()
            response_data = {'message': 'Successful operation'}
            response_headers = {'Location': f'http://localhost:8000/api/v1/users/{user_profile.id}'}
            return Response(status=status.HTTP_201_CREATED, data=response_data, headers=response_headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    '''
    Класс LogoutView представляет собой APIView для выхода пользователя из системы. Он содержит один метод delete для обработки запроса на выход пользователя.

    Метод delete:
    - Проверяет, аутентифицирован ли текущий пользователь. Если пользователь не аутентифицирован, возвращает ответ с кодом 401 UNAUTHORIZED.
    - Выполняет выход пользователя из системы с помощью функции logout().
    - Возвращает успешный ответ с кодом 200 OK.

    Swagger документация:
    - Метод delete имеет описание возможных ответов: 204 successfull operation, 401 unauthorized.
    '''
    @swagger_auto_schema(responses={204: "successfull operation", 401:"unauthorized"})
    def delete(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        logout(request)
        return OK

class UserProfilesView(APIView):
    '''
    Класс UserProfilesView представляет собой APIView для работы с профилями пользователей.
    Он содержит два метода: get для получения списка профилей пользователей и post для создания нового профиля пользователя.

    Метод get:
    - Проверяет, аутентифицирован ли текущий пользователь. Если пользователь не аутентифицирован, возвращает ответ с кодом 401 UNAUTHORIZED.
    - Получает список профилей пользователей с помощью UPM.get().
    - Сериализует данные с помощью UserProfilesSerializer.
    - Возвращает успешный ответ с кодом 200 OK и данными всех профилей пользователей.

    Метод post:
    - Проверяет, аутентифицирован ли текущий пользователь. Если пользователь не аутентифицирован, возвращает ответ с кодом 401 UNAUTHORIZED.
    - Проверяет, является ли текущий пользователь персоналом (staff). Если нет, возвращает ответ с кодом 403 FORBIDDEN.
    - Сериализует данные запроса с помощью UserProfilesSerializer.
    - Если данные валидны, сохраняет профиль пользователя и возвращает успешный ответ с кодом 201 CREATED и информацией о созданном профиле.
    - Если данные невалидны, возвращает ответ с кодом 400 BAD REQUEST и ошибками сериализации.
    '''
    @swagger_auto_schema(responses={200: "success", 400:"bad request", 401:"unauthorized", 500:'failed'})
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user_profiles = UPM.get()
        serializer = UserProfilesSerializer(user_profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(responses={201: "created", 400:"bad request", 401:"unauthorized", 403:"forbidden", 500:'failed'},
                        request_body=openapi.Schema
                        (
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "email":openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example='email100@domain.com'
                                ),
                                "password":openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example='password'
                                ),
                                "username" : openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example='V.V.Putin'
                                ),
                                "grup" : openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example='IU7-71B'
                                )
                            },
                            required=['email', 'password', "username", "grup"]
                        ))
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.user.is_staff == False:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = UserProfilesSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            user_profile = serializer.save()
            response_data = {'message': 'Successful operation'}
            response_headers = {'Location': f'http://localhost:8000/api/v1/users/{user_profile.id}'}
            return Response(status=status.HTTP_201_CREATED, data=response_data, headers=response_headers)

        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

class SingleUserView(APIView):
    '''Класс SingleUserView представляет собой API для работы с данными отдельного пользователя.

    Метод get используется для получения информации о пользователе по его id. Требуется аутентификация пользователя.
    Метод put используется для обновления информации о пользователе. Требуется аутентификация пользователя и проверка на права доступа.
    Метод delete используется для удаления пользователя. Требуется аутентификация пользователя и проверка на права доступа.
    Метод patch используется для изменения пароля пользователя. Требуется аутентификация пользователя и проверка на права доступа.



    Метод GET:
    Описание: Получение информации о пользователе по его id
    Параметры запроса: id - идентификатор пользователя
    Успешный ответ: Код 200 и информация о пользователе
    Ошибки: 400 - неверный запрос, 401 - неавторизованный запрос, 404 - пользователь не найден, 500 - ошибка сервера

    Метод PUT:
    Описание: Обновление информации о пользователе
    Параметры запроса: id - идентификатор пользователя
    Успешный ответ: Код 204 и обновленная информация о пользователе
    Ошибки: 400 - неверный запрос, 401 - неавторизованный запрос, 403 - запрещено, 500 - ошибка сервера
    Метод DELETE:

    Описание: Удаление пользователя
    Параметры запроса: id - идентификатор пользователя
    Успешный ответ: Код 204
    Ошибки: 400 - неверный запрос, 401 - неавторизованный запрос, 403 - запрещено, 404 - пользователь не найден, 500 - ошибка сервера

    Метод PATCH:
    Описание: Изменение пароля пользователя
    Параметры запроса: id - идентификатор пользователя
    Успешный ответ: Код 204 и измененный пароль пользователя
    Ошибки: 400 - неверный запрос, 401 - неавторизованный запрос, 403 - запрещено, 404 - пользователь не найден, 500 - ошибка сервера'''
    @swagger_auto_schema(responses={200: "success", 400:"bad request", 401:"unauthorized",404:"Not found", 500:'failed'})
    def get(self, request, id=None):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if id is None or id < 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user_profile = UPM.get(id)
        if not user_profile:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfilesSerializer(user_profile[0])
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={201: "created", 400:"bad request", 401:"unauthorized", 403:"Not permitted", 500:'failed'},
                        request_body=openapi.Schema
                        (
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "email":openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example='email100@domain.com'
                                ),
                                "password":openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example='password'
                                ),
                                "username" : openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example='V.V.Putin'
                                ),
                                "grup" : openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example='IU7-71B'
                                ),
                                "is_staff" : openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN,
                                    example=False
                                )
                            },
                            required=['email', 'password', "name", "group", "is_staff"]
                        ))
    def put(self, request, id=None):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if not request.user.is_staff and request.user.id != id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if id is None or id < 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user_profile = UPM.get(id=id)[0]
        if not user_profile:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfilesSerializer(instance=user_profile,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update()
            return Response(serializer.validated_data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: "success", 401:"unauthorized", 403:"Not permitted", 404:"Not found", 500:'failed'})

    def delete(self, request, id=None):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if not request.user.is_staff and request.user.id != id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if id is None or id < 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user_profile = UPM.get(id=id)
        if user_profile is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user_profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={201: "created", 400:"bad request", 401:"unauthorized", 403:"Not permitted", 500:'failed'},
                        request_body=openapi.Schema
                        (
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "old_password":openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example='password'
                                ),
                                "password":openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example='password1'
                                )
                            },
                            required=["old_password", "new_password"]
                        ))

    def patch(self, request, id=None):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if not request.user.is_staff and request.user.id != id:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if id is None or id < 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user_profile = UPM.get(id=id)[0]
        if not user_profile:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfilesSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():

            serializer.password_update()
            return Response(serializer.validated_data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
        
class SingleTaskView(APIView):
    '''
    Класс SingleTaskView представляет собой API для работы с отдельным заданием.

    Метод GET:
    URL: /tasks/{id}/
    Описание: Получает информацию о задании по его идентификатору.
    Параметры:
    id (обязательный): идентификатор задания Ответы:
    200: успешное выполнение запроса, возвращает данные задания
    401: пользователь не авторизован
    403: пользователь не имеет прав доступа
    404: задание не найдено
    500: ошибка сервера

    Метод DELETE:
    URL: /tasks/{id}/
    Описание: Удаляет задание по его идентификатору.
    Параметры:
    id (обязательный): идентификатор задания Ответы:
    200: успешное выполнение запроса, задание было удалено
    401: пользователь не авторизован
    403: пользователь не имеет прав доступа
    404: задание не найдено
    500: ошибка сервера
    '''
    @swagger_auto_schema(responses={200: "success", 401:"unauthorized", 404:"Not found", 500:'failed'})
    def get(self, request, id):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if not request.user.is_staff and not request.user.grup != "Teacher":
            return Response(status=status.HTTP_403_FORBIDDEN)
        if id is None or id < 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        task = TM.get(id)
        if not task:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TasksSerializer(task[0])
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(responses={200: "success",401:"unauthorized", 403:"Not permitted", 404:"Not found", 500:'failed'})
    def delete(self, request, id):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if not request.user.is_staff and not request.user.grup != "Teacher":
            return Response(status=status.HTTP_403_FORBIDDEN)
        if id is None or id < 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        task = TM.get(id=id)
        if task is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
 