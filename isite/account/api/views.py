from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from django.contrib.auth import authenticate

from account.api.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token


@api_view(['POST'],)
@permission_classes((AllowAny, ))
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        data['response'] = 'Successfully registered a new user.'
        data['username'] = user.username
        data['token'] = Token.objects.get(user=user).key
        data['isAdminUser'] = user.is_superuser
    else:
        data = serializer.errors
    return Response(data)


class ObtainAuthTokenView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        context = {}

        email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            try:
                Token.objects.filter(user=user).update(key=Token.generate_key())
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            context['response'] = 'Successfully authenticated.'
            context['pk'] = user.pk
            context['token'] = token.key
            context['isAdminUser'] = user.is_superuser
        else:
            context['response'] = 'Error'
            context['error_message'] = 'Invalid Credentials'

        return Response(context)
