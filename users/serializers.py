from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=150)
    password = serializers.CharField(min_length=3, max_length=10)
    confirm_password = serializers.CharField(min_length=3, max_length=10)
    email = serializers.EmailField()

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError('User already exists!')

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise ValidationError('Passwords do not match!')
        return data

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=150)
    password = serializers.CharField(min_length=3, max_length=10)


class SmsCodeSerializer(serializers.Serializer):
    SMS = serializers.CharField(min_length=6, max_length=6)

class UserAuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()
