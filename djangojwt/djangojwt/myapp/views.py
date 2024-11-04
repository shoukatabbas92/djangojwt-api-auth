from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import RegisterSerializer,LoginSerializer,UserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self,request,*args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_serializer =   UserSerializer(user)
            return Response({
                'refresh': str(refresh),
                'access' : str(refresh.access_token),
                'user'   : user_serializer.data
            })
        else:
            return Response({'detail':'invalid Credentials'},status=401)

class DashboardView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        user = request.user
        user_serializer = UserSerializer(user)
        return Response({
            'Message':'Welcome to Dashboard',
            'user' : user_serializer.data
        },200)