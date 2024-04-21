from lms.forms.forms import *
from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse

from django.contrib.auth.models import AnonymousUser

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from lms.responses import *
from django.contrib.auth import logout
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from lms.serials.sers import UserProfilesSerializer, UserAuthSerializer, TasksSerializer, TaskPacksSerializer, TaskPacksModelSerializer, SolutionsModelSerializer, SolutionsSerializer

from lms.boot import *

class TasksView(APIView):
    # permission_classes
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
