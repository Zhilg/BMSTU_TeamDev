from rest_framework import serializers
from lms.models.models import UserProfiles
from django.contrib.auth import logout, login
from lms.backends import EmailBackend
from lms.boot import *

class UserAuthSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=80, write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            try:
                user = UPM.auth_user(email, password, self.context.get("request"))
            except ValueError:
                raise serializers.ValidationError("Неправильные логин или пароль")
        else:
            message = 'Пожалуйста, укажите имя пользователя и пароль.'
            raise serializers.ValidationError(message)

        attrs['user'] = user
        return attrs

class UserProfilesSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(max_length=80, write_only=True)
    new_password = serializers.CharField(max_length=80, write_only=True)
    class Meta:
        model = UserProfiles
        manager = UPM
        fields = ("email", "password", "username", "grup", "is_staff", "last_login", "old_password", "new_password")
        
        def __str__(self):
            return self.email

    def create(self, validated_data):
        return self.Meta.manager.create(validated_data)

    def update(self):
        return self.Meta.manager.update(instance=self.instance, validated_data=self.validated_data)
    
    def password_update(self):
        try:
            return self.Meta.manager.change_password(instance=self.instance, validated_data=self.validated_data)
        except ValueError:
            raise serializers.ValidationError("Неправильный пароль")

class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        manager = TM
        fields = ("filename", "theme")
        
        def __str__(self):
            return self.filename

    def create(self, validated_data):
        return self.Meta.manager.create(validated_data)


class TaskPacksSerializer(serializers.Serializer):
    n = serializers.IntegerField()
    duetime = serializers.DateField()
    group = serializers.CharField(max_length=80)
    theme = serializers.CharField(max_length=80)
    maxgrade = serializers.IntegerField()
    mingrade = serializers.IntegerField()
    class Meta:
        manager = TPM
        
    def create(self, validated_data):
        return self.Meta.manager.create(validated_data, self.context["user"])
    
class TaskPacksModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskPacks
        fields = "__all__"
        manager = TPM
    
class SolutionsModelSerializer(serializers.ModelSerializer):
    class Meta:
        manager = SM
        model = Solutions
        fields = "__all__"
        
        
    def update(self):
        return self.Meta.manager.update(self.validated_data, self.instance)
        
class SolutionsSerializer(serializers.Serializer):
    taskpackid = serializers.IntegerField()
    filename = serializers.CharField(max_length=80)
    
    class Meta:
        manager = SM
    
    def create(self, validated_data):
        return self.Meta.manager.create(self.context["user"], validated_data)

    
    