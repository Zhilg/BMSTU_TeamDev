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