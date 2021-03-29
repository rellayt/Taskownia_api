from rest_framework import serializers
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime
import bcrypt
from django.forms.models import model_to_dict

from .serializers import UserSerializer
from .utils import createJwtToken, hashPassword, comparePassword
from .models import User
from django.core import serializers


# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        hashedPassword = hashPassword(request.data['password'])
        user = User(name=request.data['name'], email=request.data['email'], password=hashedPassword)
        user.save()
        token = createJwtToken(str(user.id))
        # userJson = serializers.serialize('json', user)
        # serializer = UserSerializer(data=request.data)
        # serializer.is_valid(raise_exception=False)
        # serializer.save()
        # return Response(serializer.data)
        data = model_to_dict(user)
        return Response({
            'token': token,
            'user': data
        })


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not comparePassword(request.data['password'], user.password):
            raise AuthenticationFailed('Incorrect password!')

        token = createJwtToken(str(user.id))

        return Response({
            'token': token,
            'user': model_to_dict(user)
        })


class UserView(APIView):
    def get(self, request):
        # token = request.headers['x-auth-token']
        # token = request.COOKIES.get('token')
        # token = request.data.jwt
        # user = User.objects.filter(id=payload['id']).first()
        # serializer = UserSerializer(user)
        return Response()
        # return Response(serializer.data)
