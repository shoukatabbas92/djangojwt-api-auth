from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserRole


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','date_joined')

class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.CharField(write_only=True,required=False)
    class Meta:
        model = User
        fields = ('username','email','password','role')

    def create(self,validted_data):
        role_name = validted_data.pop('role',None)
        user = User.objects.create_user(
            validted_data['username'],
            validted_data['email'],
            validted_data['password'],
        )
        if role_name:
            role, created = User.objects.get_or_create(name=role_name)
            UserRole.objects.create(user=user,role=role)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True,write_only=True)
