from bd_course.BaseRep import BaseRep
from lms.models.models import *
from lms.exceptions import *
from random import choices
from datetime import date

class UserProfilesRepository(BaseRep):
    def __init__(self):
        self.model = UserProfiles
        
    def get(self, user_id=None, email=None):
        if user_id is not None:
            return self.model.objects.filter(pk=user_id)
        if email is not None:
            return self.model.objects.filter(email=email)
        return self.model.objects.all()
        
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email')
        instance.username = validated_data.get('username')
        instance.grup = validated_data.get('grup')
        instance.is_staff = validated_data.get('is_staff')

        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance
    
    def update_password(self, instance, validated_data):
        old = validated_data.get('old_password')
        new = validated_data.get('new_password')
        if instance.check_password(old):
            instance.set_password(new)
            instance.save()
            return instance
        else:
            raise ValueError
    
    def insert(self, form, **extra_fields):
        email = form['email']
        username = form['username']
        grup = form['grup']
        password = form['password']
        
        user = self.model(
        email=email,
        username=username,
        grup=grup,
        **extra_fields
        )
        user.set_password(password)
        user.save()
        return user