from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Profile
from rest_framework.permissions import AllowAny
from rest_framework import generics
from .serializers import  MyTokenObtainPairSerializer, RegisterSerializer
# Create your views here.


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class =MyTokenObtainPairSerializer
    


class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny, )    
    serializer_class = RegisterSerializer