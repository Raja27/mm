__author__ = 'rajaprasanna'
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

import datetime
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.forms import default_token_generator
from django.contrib.auth.hashers import make_password
from django.views.decorators.cache import never_cache

from core import serializers
from core import models


class TokenValidate(APIView):
    """
    Just for validate Token
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        return Response({}, status.HTTP_200_OK)



class Signup(APIView):

    def post(self, request, *args, **kwargs):
        response = dict()
        code = status.HTTP_400_BAD_REQUEST
        serializer = serializers.SignupSerializer(data=request.data)
        try:
            if serializer.is_valid():
                user = serializer.save()
                print(user)
                user = authenticate(username=user.username, password=request.data.get('password'))
                print(user)
                login(request, user)
                response.update({'user': serializer.data,
                                 })
                code = status.HTTP_201_CREATED
            else:
                print(serializer.errors)
                response.update({'errors': serializer.errors})
        except Exception as e:
            print(e)
        print(response)
        return Response(response, code)


class Login(APIView):

    def post(self, request, *args, **kwargs):
        response = dict()
        code = status.HTTP_400_BAD_REQUEST
        data = request.data.copy()
        print(request.data)
        status_message = "Invalid user credentials"
        try:
            serializer = serializers.LoginSerializer(data=request.data)
            if serializer.is_valid():
                print('valid')
                username = serializer.data.get('mobile').strip()
                password = serializer.data.get('password')
                user_exists = models.User.objects.filter(mobile=username).exists()
                if not user_exists:
                    status_message = "Invalid user"  # There is no account associated with this email id.
                    code = status.HTTP_401_UNAUTHORIZED
                else:
                    username = models.User.objects.get(mobile=username).username
                    print(username, password)
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        if user.is_active:
                            if True:  # not user.is_locked and user.approved:
                                login(request, user)
                                user.last_login = datetime.datetime.now()
                                user.save()
                                user.retry_count = 0
                                user.last_login_ip = request.META.get('client_address', '')
                                user.save()
                                user_data = serializers.UserSerializer(user).data
                                status_message = 'Successfully logged in.'
                                response.update({'user': user_data,
                                                 'auth_token': user.get_auth_token(),
                                                 "verification": True,
                                                 "server_time": datetime.datetime.now()
                                                 })
                                code = status.HTTP_201_CREATED
                            else:
                                status_message = "Your account is locked out."
                                code = status.HTTP_206_PARTIAL_CONTENT
                        else:
                            status_message = "Your account is inactive."
                            code = status.HTTP_206_PARTIAL_CONTENT
                    else:
                        print('User', user)
                        code = status.HTTP_206_PARTIAL_CONTENT
                        status_message = "Invalid user credentials"
            else:
                code = status.HTTP_206_PARTIAL_CONTENT
                print('error', serializer.errors)
        except Exception as e:
            print(e)
        response.update({'status_message': status_message})
        return Response(response, code)


class Logout(APIView):
    def post(self, request, *args, **kwargs):
        response = dict()
        code = status.HTTP_400_BAD_REQUEST
        data = request.data.copy()
        print(data)
        status_message = "Logged out"
        try:
            user = request.user
            logout(request)
            user.change_auth_token()
            code = status.HTTP_201_CREATED
        except Exception as e:
            print(e)
        response.update({'status_message': status_message})
        return Response(response, code)