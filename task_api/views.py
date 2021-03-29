from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime
from .utils import createJwtToken

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        print(request.data['name'])
        print(request.data['email'])
        print(request.data['password'])
        # serializer = UserSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # return Response(serializer.data)
        return Response()

class LoginView(APIView):
    def post(self, request):
        # print(request.data['email'])
        # password = request.data['password']
        #
        #
        # if user is None:
        #     raise AuthenticationFailed('User not found')
        #
        # if not user.check_password(password):
        #     raise AuthenticationFailed('Incorrect password!')
        # user = {
        #     id: 1
        # }

        # email = request.data['email']
        # user = User.objects.filter(email=email).first()
        # token = createJwtToken(user.id)
        response = Response()
        # response.set_cookie(key='jwt', value=token, httponly=True, domain='http://3o5sc.csb.app')
        response.data = {
            # 'token': token,
            'user': request.decoded_user
        }
        return response

class UserView(APIView):
    def get(self, request):
        # token = request.headers['x-auth-token']
        # token = request.COOKIES.get('token')
        # token = request.data.jwt
        # user = User.objects.filter(id=payload['id']).first()
        # serializer = UserSerializer(user)
        return Response()
        # return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
