from tokenize import Token

from django.core.mail import send_mail
from django.db.migrations import serializer
from django.template.defaultfilters import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView

from users.models import SmsCode
from users.serializers import UserCreateSerializer, UserAuthSerializer, UserLoginSerializer, SmsCodeSerializer
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView


class RegisterAPIView(APIView):
    def post(self, request):
    # username = request.data.get('username')
    # password = request.data.get('password')
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(
            username = serializer.validated_data.get['username'],
            password = serializer.validated_data.get['password'],
            email = serializer.validated_data.get['email'],
            is_active = False
        )
        code = ''.join([str(random.randint(0,9)) for  i in range(6)])
        SmsCode.objects.create(code = code, user = user)
        send_mail(
            'Your code',
            message=code,
            from_email='<EMAIL>',
            recipient_list=[user.email]
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    # user = User.objects.create_user(username=username, password=password, email=email, is_active=False)
    # return Response(data={'user_id': user.id}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED, data={'error': 'Invalid user or password'})

class ConfirmSmsView(APIView):
    def post(self, request):
        serializer = SmsCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['SMS']
        try:
            sms = SmsCode.objects.get(code=code)
        except SmsCode.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Invalid code'})
        sms.is_active = True
        sms.user.save()
        sms.delete()
        return Response(data={'active': True}, status=status.HTTP_200_OK)


class AuthAPIView(APIView):
    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # username = serializer.validated_data.get('username')
        # password = serializer.validated_data.get('password')
        # user =  authenticate(username=username, password=password, email=email)

        user =  authenticate(**serializer.validated_data)  # - упрощенный вариант без закоментированных
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})
        return Response(data={'error': 'User not valid!'}, status=status.HTTP_401_UNAUTHORIZED)
