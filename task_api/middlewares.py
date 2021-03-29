import jwt
from rest_framework.exceptions import AuthenticationFailed


class CustomCorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "*"

        # Code to be executed for each request/response after
        # the view is called.

        return response

class JwtDecodeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        endpoint = request.path.split('/')[2]

        if (endpoint != 'login') and (endpoint != 'register'):
            request_headers = getattr(request, '_headers', request.headers)
            if hasattr(request_headers, 'X-Auth-Token'):
                token = request_headers['X-Auth-Token']
                try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
                except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!')

                # Tu sobie znajdź usera po id
                # user = User.objects.filter(id=payload['id']).first()
                # serializer = UserSerializer(user)
                # if user is None:
                #     raise AuthenticationFailed('Token is invalid')

                # A następnie przypisz go do requestu
                # request.decoded_user = user
            else:
                raise AuthenticationFailed('No Token')


