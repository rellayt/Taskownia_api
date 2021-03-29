from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import serializers
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime
import bcrypt
from django.forms.models import model_to_dict

from .serializers import UserSerializer, ProjectSerializer
from .utils import createJwtToken, hashPassword, comparePassword
from .models import User, Address, PersonalData, Project
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
        # serializer_context = {
        #     'request': request,
        # }
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def post(self, request):
        user = request.decoded_user
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
            persDataHook.first_name = request.data['first_name']
        if 'last_name' in request.data:
            persDataHook.last_name = request.data['last_name']
        if 'phone' in request.data:
            persDataHook.phone = request.data['phone']
        # TODO
        if 'birth_date' in request.data:
            b = request.data['birth_date'].split(".")
            bd = datetime.datetime(int(b[2]), int(b[1]), int(b[0]))
            persDataHook.birth_date = bd
        if 'city' in request.data:
            addrHook.city = request.data['city']
        if 'state' in request.data:
            addrHook.state = request.data['state']
        if 'country' in request.data:
            addrHook.country = request.data['country']
        if 'zip_code' in request.data:
            addrHook.zip_code = request.data['zip_code']
        userHook.update(updated_at=datetime.datetime.now())
        persDataHook.save()
        addrHook.save()
        return Response()


class ProjectsView(APIView):
    def get(self, request):
        projectSet = Project.objects.all()
        serializer = ProjectSerializer(projectSet, many=True)
        return Response(serializer.data)


class NewProjectView(APIView):
    def post(self, request):
        user = request.decoded_user
        proj = Project(author=user, title=request.data['title'], desc=request.data['desc'])
        proj.save()
        return Response()


class TakeProjectView(APIView):
    def post(self, request):
        user = request.decoded_user
        project_id = request.data['projId']
        Project.objects.filter(id=project_id).update(maker=user)
        return Response()


class MyProjectView(APIView):
    def get(self, request):
        user = request.decoded_user
        projList = Project.objects.filter(maker=user.id)
        serializer = ProjectSerializer(projList, many=True)
        return Response(serializer.data)


class MyAuthorProjectView(APIView):
    def get(self, request):
        user = request.decoded_user
        projList = Project.objects.filter(author=user.id)
        serializer = ProjectSerializer(projList, many=True)
        return Response(serializer.data)


