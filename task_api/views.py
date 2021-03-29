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
from .models import User, Address, PersonalData
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
        # token = request.headers['X-Auth-Token']
        # token = request.COOKIES.get('token')
        # token = request.data.jwt
        # user = User.objects.filter(id=payload['id']).first()
        user = request.decoded_user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def post(self, request):
        user = request.decoded_user
        # userData = User.objects.get(pk=user.id)
        # tu jest cudo, bo aktualizuje wszystkich z tym ID, ale id jest unikatowe wiec niby spoko
        userHook = User.objects.filter(id=user.id)
        persDataHook = userHook.first().personal_data
        addrHook = userHook.first().address
        if persDataHook is None:
            persDataHook = PersonalData()
            persDataHook.save()
            userHook.update(personal_data=persDataHook)
        if addrHook is None:
            addrHook = Address()
            addrHook.save()
            userHook.update(address=addrHook)
        if 'name' in request.data:
            userHook.update(name=request.data['name'])
        if 'email' in request.data:
            userHook.update(email=request.data['email'])
        if 'password' in request.data:
            userHook.update(password=hashPassword(request.data['password']))
        if 'first_name' in request.data:
            # if persDataHook is None:
            #     pers_data = PersonalData(first_name=request.data['first_name'])
            #     pers_data.save()
            #     User.objects.filter(id=user.id).update(personal_data=pers_data)
            # else:
            #     persDataHook.first_name=request.data['first_name']
            #     persDataHook.save()
            persDataHook.first_name = request.data['first_name']
        if 'last_name' in request.data:
            persDataHook.last_name = request.data['last_name']
        if 'phone' in request.data:
            persDataHook.phone = request.data['phone']
        # TODO
        if 'birth_date' in request.data:
            b = request.data['birth_date'].split(".")
            bd = datetime.datetime(b[2], b[1], b[0])
            persDataHook.birth_date = bd
        if 'city' in request.data:
            addrHook.city = request.data['city']
        if 'state' in request.data:
            addrHook.state = request.data['state']
        if 'country' in request.data:
            addrHook.country = request.data['country']
        if 'zip_code' in request.data:
            addrHook.zip_code = request.data['zip_code']
        # userHook.update(updated_at=datetime.now)
        # userHook.updated_at = datetime.now()
        persDataHook.save()
        addrHook.save()


        # print(userData)

        # serializer = UserSerializer(data=user)
        # serializer.is_valid()
        # print(serializer.data)
        # # print(serializer)
        # serializer.data.name = request.data['name']
        # # print(serializer)
        # if serializer.is_valid():
        #     print('yeah')
        #     serializer.save()
        # else:
        #     print(serializer.errors)
        return Response("SUCCESS")


class UserDataView(APIView):
    def get(self, request):
        return Response()